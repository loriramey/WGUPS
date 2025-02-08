#author info: Student ID 010899261, Loretta ("lori") Ramey
#built in Python 9.3.21
#Main program execution happens here: orchestration of events, initialize UI

from datetime import datetime
import os
import logging
from app_wgups.distance_matrix import load_distance_data
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.truck import Truck
from app_wgups.ui import user_interface

#---IMPLEMENT A LOGGING PROCESS TO CATCH ALL ERRORS AND LOGS, PRINT CRITICAL ERRORS TO CONSOLE
logging.basicConfig(
    filename="wgups_debug.log",  # Log file name
    level=logging.DEBUG,  # Capture all debug, info, warning, and error messages
    format="%(asctime)s [%(levelname)s] %(message)s",  # Include timestamp
    filemode="w",  # Overwrite log file on each run (use "a" to append instead)
)
# Create a second handler to print only errors to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)

# Add the handler to the root logger
logging.getLogger().addHandler(console_handler)


#------------------------MAIN PROGRAM LOGIC------------------------------

# Load and initialize the first 2 trucks of the day
def load_all_data():
    """
    Loads package and distance data, initializes first 2 trucks, and prepares routes.
    This function:
      - Loads package data from a CSV file into a hash table.
      - Loads the distance matrix for route calculations.
      - Initializes the first two delivery trucks.
      - Sets their departure times and optimizes their delivery routes using the Nearest Neighbor algorithm.
    Args:
        None
    Returns:
        tuple: (HashTable, dict, list) containing:
            - package_hash (HashTable): A hash table storing all package data.
            - distance_matrix (dict): The distance matrix used for routing.
            - trucks (list of Truck): The initialized trucks with assigned delivery manifests.
    """
    global package_hash, distance_matrix, trucks

    #Force data to load correctly from the root folder of the project regardless of user operating system
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    CSV_FILE_PATH_PACKAGES = os.path.join(DATA_DIR, "packages_data.csv")
    CSV_FILE_PATH_DISTANCES = os.path.join(DATA_DIR, "distance_matrix.csv")

    # Debug logging
    logging.info(f"Looking for data in: {DATA_DIR}")
    logging.info(f"Checking: {CSV_FILE_PATH_DISTANCES}")

    # Load package data into hash table
    package_hash = HashTable()
    Package.load_package_data(CSV_FILE_PATH_PACKAGES, package_hash)

    # Load distance matrix for use in calculating NN algo
    distance_matrix = load_distance_data(CSV_FILE_PATH_DISTANCES)

    # Initialize first 2 Trucks
    trucks = [Truck(1), Truck(2)]

    # Truck 1 departs at 9:10, Truck 2 at 8:05
    trucks[0].departure_time = datetime.strptime("09:06", "%H:%M")
    trucks[1].departure_time = datetime.strptime("08:01", "%H:%M")

    # Load and optimize Truck 1 & 2's delivery manifests
    for truck in trucks:
        truck.load_package(package_hash, truck.departure_time)
        truck.calculate_delivery_route(distance_matrix)

    logging.info("Truck 1 & 2 loaded and optimized.")

    return package_hash, distance_matrix, trucks


#--------**Run the Full Package Delivery Day Simulation**------------

def run_delivery_simulation():
    """
    Runs the full package delivery simulation for all three trucks.
    This function:
      - Loads and initializes package and truck data.
      - Simulates deliveries for Truck 1 and Truck 2.
      - Ensures both trucks return to the hub before Truck 3 departs.
      - Handles special case: Package 9's incorrect address update at 10:20 AM.
      - Simulates deliveries for Truck 3.
    Args:
        None
    Returns:
        tuple: (HashTable, list) containing:
            - package_hash (HashTable): The hash table storing package data.
            - trucks (list of Truck): The list of all trucks after deliveries are completed.
    """
    package_hash, distance_matrix, trucks = load_all_data()

    # Run Truck 1 & 2 Deliveries
    for truck in trucks:
        logging.info(f"Running deliveries for Truck {truck.truck_id}...")
        while truck.manifest:
            truck.deliver_package(truck.manifest[0], distance_matrix)

    #handle situation where truck is not yet back when checking return time
    truck1_return = trucks[0].return_time.strftime('%H:%M') if trucks[0].return_time else "Not Yet Returned"
    truck2_return = trucks[1].return_time.strftime('%H:%M') if trucks[1].return_time else "Not Yet Returned"

    logging.info(f"Truck 1 returned at {trucks[0].return_time.strftime('%H:%M')}, Distance: {trucks[0].distance_traveled:.2f} miles")
    logging.info(f"Truck 2 returned at {trucks[1].return_time.strftime('%H:%M')}, Distance: {trucks[1].distance_traveled:.2f} miles")

    # **Handle Truck 3 (Late Package)**
    logging.info("Truck 3 Preparing to Depart...\n")

    # Ensure Trucks 1 & 2 have returned
    for truck in trucks:
        if truck.return_time is None:
            truck.return_to_hub(distance_matrix)

    # Determine Truck 3’s departure time
    truck3_departure_time = Truck.calculate_truck3_departure(trucks[0], trucks[1], distance_matrix)

    # Initialize and load Truck 3
    truck3 = Truck(3)
    truck3.load_package(package_hash, truck3_departure_time)
    trucks.append(truck3)

    #HANDLING KNOWN ISSUE: Correct Package 9’s address at 10:20 AM when info is available
    package_9 = package_hash.lookup(9)
    package_9.update_address("410 S State St", "Salt Lake City", "UT", "84111")
    logging.info(f"\n**Package 9 Address Updated: {package_9.address}")

    # Optimize Truck 3’s route
    truck3.calculate_delivery_route(distance_matrix)

    # Run Truck 3 Deliveries
    while truck3.manifest:
        truck3.deliver_package(truck3.manifest[0], distance_matrix)

    logging.info(f"\nTruck 3 returned at {truck3.return_time.strftime('%H:%M')}, Distance: {truck3.distance_traveled:.2f} miles")

    #return values for global variables to use when running "Main"
    return package_hash, trucks


# -----------**MAIN FUNCTION**----------------
if __name__ == "__main__":
    """
    Main execution of the package delivery system.
    This script:
      - Runs the full delivery simulation for all trucks.
      - Launches the user interface after simulation completes.
    Args:
        None
    Returns:
        None: The function runs until the user exits the program.
    """
    package_hash, trucks = run_delivery_simulation()  # Runs the delivery process automatically
    user_interface(package_hash, trucks)  # Launches the CLI after simulation completes
