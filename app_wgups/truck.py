#this class creates Truck objects and data storage for truck manifests, delivery graphs
#sources used when building this code: Python datetime documentation at https://docs.python.org/3.9/library/datetime.html?highlight=time#module-datetime

from datetime import datetime, timedelta

from app_wgups.distance_matrix import get_distance
from app_wgups.package import Package
from app_wgups.routing import NearestNeighbor  # Import NN Algorithm
from app_wgups.status import PackageStatus

import logging


#create truck objects and methods to support truck movement and delivery actions
class Truck:
    #define class object variables
    def __init__(self, truck_id):
        """
        Represents a delivery truck used in the WGUPS package delivery system.
        This class models a truck with attributes for tracking its deliveries,
        location, speed, and cargo capacity.

        Attributes:
            truck_id (int): Unique identifier for the truck.
            capacity (int): Maximum number of packages the truck can carry.
            speed (float): Speed of the truck in miles per hour.
            distance_traveled (float): Total miles traveled by the truck.
            departure_time (datetime or None): The time the truck departs from the hub.
            current_location (str): The truck's current location (default: "hub").
            current_time (datetime or None): The current simulation time for the truck.
            manifest (list): List of packages assigned to the truck.
            return_time (datetime or None): The time the truck returns to the hub.
            delivery_log (list): Log of deliveries made by the truck.
        Args:
            truck_id (int): The unique ID assigned to the truck.
        Returns:
            None
        """
        self.truck_id = truck_id
        self.capacity = 16
        self.speed = 18.0  #mph
        self.distance_traveled = 0.0
        self.departure_time = None
        self.current_location = "hub"
        self.current_time = None
        self.manifest = []
        self.return_time = None
        self.delivery_log = []

    #method to load packages onto the truck - for each truck & update package departure time & status
    def load_package(self, package_hash, departure_time):
        """
        Loads packages onto the truck and updates their departure status.
        This method retrieves all packages assigned to the truck from the hash table,
        verifies that the truck does not exceed its capacity, and updates the
        status of each package to "EN ROUTE" with a recorded departure time.

        Args:
            package_hash (HashTable): The hash table storing package data.
            departure_time (str or datetime): The time the truck departs the hub.
                                              Accepts a string in "HH:MM" format
                                              or a datetime object.
        Returns:
            list: A list of Package objects loaded onto the truck.
        Raises:
            ValueError: If the number of assigned packages exceeds the truck's capacity.
        """
        delivery_list = Package.get_packages_by_truck(package_hash, self.truck_id)

        if len(delivery_list) > self.capacity:
            logging.error("Package capacity exceeded on load for Truck {self.truck_id}")
            raise ValueError(
                f"Truck {self.truck_id} overloaded! Capacity is {self.capacity}, "
                f" but {len(delivery_list)} packages were assigned.")

        #create a list of packages to be delivered
        self.manifest = delivery_list

        #set departure time for truck and start tracking "current time" as it moves along its route
        if isinstance(departure_time, str):
            departure_time = datetime.strptime(departure_time, "%H:%M")
        self.departure_time = departure_time
        self.current_time = departure_time

        #update status of all packages to EN_ROUTE, update package departure time
        for package in self.manifest:
            package.update_status(PackageStatus.EN_ROUTE)
            package.update_departure_time(departure_time)

        return self.manifest


    #method to determine best route for delivery via NN algo
    def calculate_delivery_route(self, distance_matrix):
        """
        Optimizes the truck's delivery route using the Nearest Neighbor algorithm.
        This method determines the most efficient order of deliveries based on
        distance calculations. If no packages are assigned to the truck,
        a log entry is recorded and no optimization is performed.

        Args:
            distance_matrix (dict): A nested dictionary representing distance
                                    values between delivery locations.
        Returns:
            list: The optimized list of Package objects, reordered for delivery efficiency.
        """
    
        if not self.manifest:  #debugging
            logging.info(f"Truck {self.truck_id} has no packages to deliver.")
            return

        logging.info(f"Optimizing route for Truck {self.truck_id}...")

        #run algo & return optimized package list as the new truck manifest
        optimized_route = NearestNeighbor(self, distance_matrix).calculate_NN_route(self)
        self.manifest = optimized_route
        return self.manifest


    #helper method to update specific delivery time for packages when delivered
    def calculate_delivery_time(self, package, distance_matrix):
        """
        Calculates and updates the expected delivery time for a package.

        This method determines how long it will take the truck to reach
        the package’s destination from its current location. If the truck
        is already at the delivery location, the package is marked as
        delivered immediately. If the truck must travel, the method
        calculates travel time based on distance and speed, then updates
        the package’s delivery time accordingly.

        If a package has a deadline and will be delivered late, a warning
        message is displayed.

        Args:
            package (Package): The package to be delivered.
            distance_matrix (dict): A nested dictionary representing distance
                                    values between delivery locations.
        Returns:
            datetime: The expected delivery time for the package, or None
                      if distance data is unavailable.
        """
        if self.current_location is None:  #error handling if no location
            logging.error(f"Truck {self.truck_id} has no current location set")
            raise ValueError(f"Truck {self.truck_id} has no current location set!")

        #handle cases where truck is already at proper location to deliver
        if self.current_location == package.address:
            package.update_delivery_time(self.current_time)
            return package.delivery_time

        else:  #normal delivery (truck had to move to get here)
            distance = get_distance(distance_matrix, self.current_location, package.address)

            if distance is None:  #error handling for a missing address pair on adjacency matrix
                logging.error(f"ERROR Distance from {self.current_location} to {package.address} not found in matrix for package {package.package_id}")
                return None

            #delivery time for packages is calculated based on distance between points and truck speed
            travel_time = timedelta(minutes=(distance / self.speed) * 60)
            delivery_time = self.current_time + travel_time
            package.update_delivery_time(delivery_time)  #update package details

            #issue warning if package will be LATE
            if package.deadline != "23:59":
                deadline_time = package.deadline
                if delivery_time.time() > deadline_time:
                    print(f"WARNING! Package {package.package_id} at {package.address} will be late. | "
                          f"Projected delivery time is {delivery_time.strftime('%H:%M')}. ")

            return delivery_time


    #method to "deliver" package by updating package status & delivery time, move from truck manifest to log
    def deliver_package(self, package, distance_matrix):
        """
        Delivers a package by updating its status, logging delivery time, and
        updating the truck's manifest and movement.

        This method simulates the process of delivering a package:
        - Checks if the truck has any packages left; if not, returns to the hub.
        - Handles known incorrect address cases (e.g., Package 9 before 10:20 AM).
        - Calls `calculate_delivery_time` to determine when the package was delivered.
        - Updates package status to DELIVERED and records the delivery in the truck log.
        - Updates truck's location and total distance traveled.
        - Implements error handling for missing distance data and ensures delivery time is set.

        Args:
            package (Package): The package object to be delivered.
            distance_matrix (dict): The distance matrix used to calculate travel distances.
        Returns:
            None: Modifies package and truck attributes in place.
        """
        if not self.manifest:
            logging.info(f"Truck {self.truck_id} has no more packages to deliver. Returning to hub.")
            self.return_to_hub(distance_matrix)
            return

        #handling bad address for package 9 without crashing the program
        if package.package_id == 9 and self.current_time < datetime.strptime("10:20", "%H:%M"):
            logging.info(f"ERROR: Package 9 has an incorrect address ({package.address}). "
                  f"Delivery not possible until 10:20 AM!")
            return  # Skip this delivery attempt

        delivery_time = self.calculate_delivery_time(package, distance_matrix)

        # DEBUG: Log package status before delivery
        logging.debug(f"Before Delivery | Truck {self.truck_id} Package {package.package_id} "
              f"Status: {package.status}, Delivery Time: {package.delivery_time}")

        # Update package status & delivery time, update truck delivery time log
        package.update_status(PackageStatus.DELIVERED)
        package.update_delivery_time(delivery_time)
        self.current_time = delivery_time  # Update truck's "current time"

        # Handle deliveries at the same location (truck did not move)
        if self.current_location == package.address:
            logging.info(f"Package {package.package_id} is already at {package.address}. Delivered instantly!")

        # else normal delivery location updates
        else:
            # Calculate movement and update truck location variables
            distance = get_distance(distance_matrix, self.current_location, package.address)

            #FOR TESTING & DEBUGGING
            # Get distance from current location to package destination
            if distance is None:  # If distance is missing in the adjacency matrix
                logging.warning(f"WARNING: Truck {self.truck_id} Distance from {self.current_location} to {package.address} not found")
                logging.info(f"Skipping Package {package.package_id} and moving to next package.")
                return  # Skip delivery if distance is undefined

            self.distance_traveled += distance  # Track total miles traveled at this point on route
            self.current_location = package.address  # Truck location set to this address ahead of next move

        # FOR TESTING Ensure package has a valid delivery time
        if package.delivery_time is None:  # Still None? Try to force re-calculation
            logging.error(f"ERROR:Package {package.package_id} has no delivery time after calculation!")
            package.delivery_time = self.calculate_delivery_time(package, distance_matrix)

        # Final safety check before moving on in implementation
        if package.delivery_time is None:
            logging.error(f"CRITICAL ERROR: Package {package.package_id} still has no delivery time! Using fallback time.")
            package.delivery_time = self.current_time  # Assign the truck's current time as a last resort

        # Update truck manifest & logs
        self.delivery_log.append((package.package_id, delivery_time))
        self.manifest.remove(package)

        # DEBUG: Confirm package was delivered
        logging.info(f"Truck {self.truck_id} Delivered Package {package.package_id} at {delivery_time.strftime('%H:%M')} | "
              f"(Miles Traveled: {self.distance_traveled:.2f}) | Package Status: {package.status}")

        # Check if truck should return to hub
        if not self.manifest:
            self.return_to_hub(distance_matrix)


    #method to send truck back to hub when manifest is empty, record final return time
    def return_to_hub(self, distance_matrix):
        """
        Sends the truck back to the hub when all packages have been delivered.
        This function calculates the distance from the truck's current location
        to the hub, determines the time required to travel that distance, and
        updates the truck's return time. It also logs relevant details such as
        the total distance traveled and the number of packages delivered.

        Args:
            distance_matrix (dict): The distance matrix used to calculate distances
                                    between locations.
        Returns:
            datetime: The time the truck returns to the hub.
        """
        if not self.manifest:  #if manifest is empty
            distance_to_hub = get_distance(distance_matrix, self.current_location, "hub")                             # calculate distance from last stop to hub
            travel_time = timedelta(minutes=(distance_to_hub / self.speed) * 60)
            self.return_time = self.current_time + travel_time  # add that time to overall accumulated time

            #FOR TESTING
            package_count = len(self.delivery_log)
            logging.info(f"Truck {self.truck_id} returned to hub at {self.return_time.strftime('%H:%M')},"
                  f" total distance traveled: {self.distance_traveled:.2f} miles.")
            logging.info(f"Truck delivered {package_count} packages.")
            logging.info(f"{self.delivery_log}")

            return self.return_time


    #helper method to determine time for truck 3 to leave
    def calculate_truck3_departure(truck1, truck2, distance_matrix):
        """
        Determines the departure time for Truck 3 based on when the first two trucks return.
        This function ensures that Truck 3 does not leave until at least one of the first
        two trucks has returned to the hub. It calculates the earliest return time between
        Truck 1 and Truck 2 and sets Truck 3's departure time to 15 minutes after that.

        Args:
            truck1 (Truck): The first delivery truck.
            truck2 (Truck): The second delivery truck.
            distance_matrix (dict): The distance matrix used to calculate travel times.
        Returns:
            datetime: The calculated departure time for Truck 3.
        """
        if truck1.return_time is None:     #make sure trucks have return times
            truck1.return_to_hub(distance_matrix)
        if truck2.return_time is None:
            truck2.return_to_hub(distance_matrix)

        earliest_return = min(truck1.return_time, truck2.return_time)
        # Truck 3 departs 15 minutes later
        truck3_departure = earliest_return + timedelta(minutes=15)

        return truck3_departure