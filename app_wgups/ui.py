#USER INTERFACE: functions related to running the CLI UI for end users

from datetime import datetime
import sys

from app_wgups import package
from app_wgups.distance_matrix import load_distance_data
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.status import PackageStatus
from app_wgups.truck import Truck

#INITIALIZE GLOBAL VARIABLES
package_hash = HashTable()
distance_matrix = None
trucks = []


#UI INTERFACE CODE - basic CLI interface with dictionary of options
def user_interface(package_hash, trucks):
    """
    Launches the user interface for the WGUPS Package Management System.

    This function presents a command-line interface (CLI) that allows users
    to interact with the package tracking system. Users can:
      - Lookup a single package status at a specific time
      - View all package statuses at a specific time
      - View all package statuses at the end of the delivery day
      - Exit the program

    The interface operates in a loop until the user selects the exit option.

    Args:
        package_hash (HashTable): The hash table storing all package data.
        trucks (list of Truck): A list of Truck objects representing delivery vehicles.

    Returns:
        None: Runs the CLI until the user chooses to exit.
    """
    
    #helper function for getting user inputs
    def get_valid_package_id():
        """
        Prompts the user to enter a valid package ID and validates the input.

        This function requests a package ID from the user. It ensures the input is
        a numeric value and converts it to an integer. If the input is invalid,
        an error message is displayed, and None is returned.

        Args:
            None

        Returns:
            int or None: The package ID as an integer if valid, or None if the input is invalid.
        """
        package_id = input("\nEnter Package ID#: ").strip()
        if not package_id.isdigit():
            print("ERROR: Package ID must be a number.")
            return None
        return int(package_id)

    def get_valid_time():
        """
        Prompts the user to enter a valid time and converts it into a datetime object.

        This function requests a time input from the user in HH:MM (24-hour) format.
        If the input is invalid, an error message is displayed, and None is returned.

        Args:
            None

        Returns:
            datetime or None: A datetime object representing the entered time if valid,
                              or None if the input is invalid.
        """
        check_time = input("Enter time to check in 24-hour format, HH:MM: ").strip()
        parsed_time = parse_time(check_time)  # Convert to datetime
        if parsed_time is None:
            print("ERROR: Invalid time format. Use HH:MM (24-hour).")
            return None
        return parsed_time

    #Option 1: Print single package status
    def print_single_package():
        """
        Prints the status of a single package at a user-specified time.

        This function prompts the user to enter a package ID and a time
        in HH:MM format, then retrieves and displays the status of the
        specified package at that time.

        Args:
            None

        Returns:
            None: Prints the package status directly to the console.
        """
        package_id = get_valid_package_id()  # Use helper function
        if package_id is None:
            return

        parsed_time = get_valid_time()  # Use helper function
        if parsed_time is None:
            return

        lookup_and_print_package_by_ID(package_id, package_hash, parsed_time)

    #Option 2: Print all package statuses
    def print_all_packages():
        """
        Prints the status of all packages at a user-specified time.

        This function prompts the user to enter a time in HH:MM format
        and then retrieves and displays the status of all packages
        at that specific time.

        Args:
            None

        Returns:
            None: Prints the package statuses directly to the console.
        """
        parsed_time = get_valid_time()
        if parsed_time is None:
            return
        display_all_package_statuses(package_hash, trucks, parsed_time)

    #Option 3: Print end-of-day status
    def print_eod_status():
        """
        Prints the end-of-day status for all packages.

        This function retrieves and displays the status of all packages
        as of 18:00 (6:00 PM), showing their final state at the end of the
        delivery day.

        Args:
            None

        Returns:
            None: Prints the package statuses directly to the console.
        """
        print("\nEOD Status of all Packages:\n")
        display_all_package_statuses(package_hash, trucks, "18:00")

    #Option 4: Exit the program
    def exit_program():
        """
        Terminates the program and prints a farewell message.

        This function gracefully exits the CLI interface by returning False,
        which signals the main menu loop to terminate.

        Args:
            None

        Returns:
            bool: Always returns False to indicate the program should exit.
        """
        print("\nExiting program. Have an awesome day!\n")
        return False

    #Menu dictionary mapping options to functions
    menu_options = {
        "1": print_single_package,
        "2": print_all_packages,
        "3": print_eod_status,
        "4": exit_program
    }

    #Print the menu in a loop
    while True:
        print("\n**********************************************")
        print("WELCOME TO THE WGUPS PACKAGE MANAGEMENT SYSTEM")
        print("**********************************************")
        print("1. Print a Single Package Status (Input a Time)")
        print("2. Print All Package Statuses and Truck Mileage (Input a Time)")
        print("3. Print All Package Statuses at EOD")
        print("4. Exit the Program")
        print("**********************************************\n")

        print("Enter your choice: ", end="", flush=True)
        choice = input().strip()

        if choice in menu_options.keys():
            if menu_options[choice]() is False:
                break
        else:
            print("\nX Invalid choice. Please try again.\n")


#helper function to turn user input clock time into a datetime object
def parse_time(user_input):
    """
    Converts a user-provided time string into a datetime object.

    This function takes a time input in the format "HH:MM" (24-hour clock)
    and converts it into a datetime object for further processing.

    Args:
        user_input (str): A time string in "HH:MM" format.

    Returns:
        datetime or None: A datetime object representing the parsed time if successful,
        or None if the input format is invalid.
    """
    try:   #convert user input into date-time object
        return datetime.strptime(user_input, "%H:%M")
    except ValueError:
        print("X ERROR: Invalid time format. Please enter a valid time in HH:MM (24-hour).")
        return None


#helper function for looking up package delivery status
def get_package_status_at_time(package, parsed_time):
    """
    Determines the status of a package at a specific time.

    This function checks whether a package is still at the hub, en route for delivery,
    or has been delivered based on its departure and delivery times.

    Args:
        package (Package): The package object whose status needs to be determined.
        parsed_time (datetime): The specific time to check the package status.

    Returns:
        str: The status of the package at the given time. Possible values:
            - "AT HUB" (if the package has not yet departed)
            - "EN ROUTE" (if the package has left the hub but not yet been delivered)
            - "DELIVERED" (if the package has already been delivered)
    """
    if package.departure_time and parsed_time < package.departure_time:
        status = "AT HUB"
    elif package.delivery_time and parsed_time >= package.delivery_time:
        status = "DELIVERED"
    else:
        status = "EN ROUTE"

    return status


#for Task 2 directions, part B: LOOKUP FUNCTION by PACKAGE ID
#helper function - lookup single package by id
def lookup_and_print_package_by_ID(package_id, hash_table, parsed_time):
    """
    Retrieves and prints the status of a package based on its ID and a given time.

    This function looks up a package in the hash table using the provided package ID,
    determines its status at the specified time, and prints relevant package details.

    Args:
        package_id (int): The unique ID of the package to look up.
        hash_table (HashTable): The hash table containing package data.
        parsed_time (datetime): The time at which to check the package status.

    Returns:
        None: The function prints the package details to the console.
    """
    package = hash_table.lookup(int(package_id))
    if not package:
        return

    if parsed_time is None or not package:  #error handling if user inputs invalid time
        print(f"Package with ID {package_id} not found")
        return

    #package9 has wrong address till 10:20am
    status = get_package_status_at_time(package, parsed_time)
    address = "300 State St (Incorrect)" if (package.package_id == 9
            and parsed_time < datetime.strptime("10:20", "%H:%M")) \
            else package.address

    #print to screen
    print(f"\nPackage {package_id} Status at {parsed_time.strftime('%H:%M')}")
    print("------------------------------------------------")
    print(f"Status: {colorize_output(status)}")
    print(f"\nDelivery Full Address: {address}, {package.city}, {package.state}, {package.zip_code}")
    print(f"\nDelivery by Truck: {package.truck} |  Package Weight: {package.weight}")
    print(f"\nDelivery Deadline: {package.deadline.strftime('%H:%M') if package.deadline else 'EOD'}")
    print(f"\nDelivery Time: {package.delivery_time.strftime('%H:%M') if package.delivery_time else 'In Transit'}")
    print("------------------------------------------------\n")



#helper function - lookup all packages by time and return status + time, and mileage for all trucks
def display_all_package_statuses(hash_table, trucks, check_time):
    """
    Displays the status of all packages at a specified time.

    This function retrieves and prints the status of all packages based on their
    delivery progress at the given time. It also calculates and displays the total
    mileage of all trucks.

    Args:
        hash_table (HashTable): The hash table storing package data.
        trucks (list): A list of Truck objects to retrieve mileage information.
        check_time (str or datetime): The time to check package statuses. Accepts
                                      a string in HH:MM format or a datetime object.

    Returns:
        None: The function prints the package statuses and total truck mileage
              to the console.
    """
    #validate whether check_time is already a date-time object or a string
    if isinstance(check_time, str):
        parsed_time = parse_time(check_time)
    else:
        parsed_time = check_time

    print("\nPackage Statuses at", parsed_time.strftime("%H:%M"), "\n")
    print("-----------------------------------------------")

    total_miles = sum(truck.distance_traveled for truck in trucks)
    package_status_list = []

    for bucket in hash_table.table:
        for _, pkg in bucket:
            status = get_package_status_at_time(pkg, parsed_time)
            address = "300 State St (Incorrect)" if pkg.package_id == 9 and parsed_time < datetime.strptime("10:20","%H:%M") else pkg.address
            if status == "DELIVERED":
                delivery_time = pkg.delivery_time.strftime('%H:%M')
                delivery_time_label = "Delivered"
            else:
                delivery_time = pkg.deadline.strftime('%H:%M')
                delivery_time_label = "Anticipated Delivery"
            truck_number = pkg.truck
            status_colored = colorize_output(status)

            package_status_list.append((
                pkg.package_id,
                f"Package {pkg.package_id}: {status_colored} on Truck {truck_number}; {delivery_time_label}: {delivery_time} to {address}"
            ))

    package_status_list.sort(key=lambda x: x[0] )

    for _, package_info in package_status_list:
        print(package_info)

    print("-----------------------------------------------\n")
    print(f"\nTotal Truck Mileage: {total_miles:.2f}")
    print("-----------------------------------------------\n")


#helper function - reset all data to start a new day
def reset_day(package_hash, trucks):
    """
    Resets all package and truck data to start a new delivery day.

    This function clears the package hash table and resets all truck attributes,
    including their manifests, delivery logs, distance traveled, and current locations.

    Args:
        package_hash (HashTable): The hash table storing package data.
        trucks (list): A list of Truck objects that need to be reset.

    Returns:
        None: This function modifies the package hash table and truck objects in place.
    """
    package_hash.clear()

    for truck in trucks:
        truck.manifest.clear()
        truck.delivery_log.clear()
        truck.distance_traveled = 0.0
        truck.current_location = "hub"
        truck.current_time = None
        truck.return_time = None

    print("System reset; all package and truck data cleared.")


#helper function: color code any results printed to screen based on package status
def colorize_output(status):
    """
    Applies color formatting to package status output in the terminal.

    This function assigns ANSI color codes to different package statuses
    to enhance readability in the console.

    Args:
        status (str): The package status, expected values are "AT HUB",
                      "EN ROUTE", or "DELIVERED".

    Returns:
        str: The status string wrapped in the appropriate ANSI color code.
    """
    colors = {
    "AT HUB": "\033[91m",  # Red
    "EN ROUTE": "\033[93m",  # Yellow
    "DELIVERED": "\033[92m",  # Green
    "RESET": "\033[0m"  # Reset color formatting
    }

    return f"{colors.get(status, colors['RESET'])}{status}{colors['RESET']}"