#this class creates Package objects and stores them in a hash table

import csv
import os
import logging
from datetime import time
from app_wgups.hash_table import HashTable
from app_wgups.status import PackageStatus

#define Packages class to create Package objects
class Package:
    #define class object variables
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes="", truck=None):
        """
        Initializes a Package object.
        This constructor sets up a Package instance with its unique identifier,
        delivery details, weight, notes, and associated truck. Default values
        are assigned for status, departure time, and delivery time.

        Args:
            package_id (int): The unique ID of the package.
            address (str): The delivery address of the package.
            city (str): The city where the package will be delivered.
            state (str): The state where the package will be delivered.
            zip_code (str): The ZIP code of the delivery address.
            deadline (str or datetime): The deadline by which the package must be delivered.
            weight (float): The weight of the package in kilograms.
            notes (str, optional): Any special delivery notes. Defaults to an empty string.
            truck (int, optional): The truck number assigned for delivery. Defaults to None.
        Attributes:
            status (PackageStatus): The current status of the package (AT_HUB by default).
            departure_time (datetime, optional): The time the package leaves the hub. Defaults to None.
            delivery_time (datetime, optional): The actual time the package is delivered. Defaults to None.
        Returns:
            None
        """
        self.package_id = package_id  # Unique ID for the package, key in hash table
        self.address = address  # Delivery address
        self.city = city  # Delivery city
        self.state = state
        self.zip_code = zip_code  # Delivery ZIP code
        self.deadline = deadline  # Delivery deadline
        self.weight = weight  # Weight in kg
        self.notes = notes  # Special delivery notes (optional)
        self.truck = truck #assigned truck number, default None

        #additional class variables set by program
        self.status = PackageStatus.AT_HUB  # Default status using enum - AT HUB
        self.departure_time = None #Time package left the hub on a truck, default None
        self.delivery_time = None  #Time of delivery (default: not delivered), default None


    #define method to load packages from the csv file
    @staticmethod
    def load_package_data(csv_filepath, hash_table):
        """
        Loads package data from a CSV file into a hash table.
        This function reads package information from a CSV file, creates `Package` objects
        for each row, and inserts them into the provided hash table.

        Args:
            csv_filepath (str): The file path to the CSV containing package data.
            hash_table (HashTable): The hash table where package objects will be stored.
        File Structure (CSV format):
            Column 0: Package ID (int)
            Column 1: Address (str)
            Column 2: City (str)
            Column 3: State (str)
            Column 4: ZIP Code (str)
            Column 5: Delivery Deadline (str in HH:MM format or 'EOD' for End of Day)
            Column 6: Weight (int)
            Column 7: Notes (str, optional)
            Column 8: Truck Assignment (int, optional)
        Processing:
            - Reads each row from the CSV.
            - Converts `deadline` from string to a `time` object, defaulting to 23:59 if "EOD".
            - Converts `weight` and `truck` values to integers where applicable.
            - Inserts each package into the `hash_table` using its `package_id` as the key.
        Returns:
            None: The function modifies the `hash_table` in place.
        """
    
        #ensure filepath to data files in project directory:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This gets the current script's directory
        DATA_DIR = os.path.join(BASE_DIR, "..", "data")  # Adjust if needed
        CSV_FILE_PATH = os.path.join(DATA_DIR, "packages_data.csv")  # Adjust file name if needed


        with open(CSV_FILE_PATH, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)

            for row in reader:  #read in a package object
                try:  #this code handles common errors with the datetime format / incorrect type errors in Deadline data
                    raw_deadline = row[5].strip()
                    deadline = time.fromisoformat(raw_deadline) if raw_deadline and raw_deadline != "EOD" else time(16,59)
                except ValueError:
                    logging.error(f"Invalid deadline format for package {row[0]}: {row[5]}. Defaulting to 16:59.")
                    deadline = time(16, 59)

                package = Package(
                    package_id=int(row[0]),
                    address=row[1],
                    city=row[2],
                    state=row[3],
                    zip_code=row[4],
                    deadline=deadline,
                    weight=int(row[6]),
                    notes=row[7] if len(row) > 7 else "",
                    truck=int(row[8]) if len(row) > 8 and row[8].strip() else None
                )
                hash_table.insert(package.package_id, package)


    # define methods to update attributes (status, delivery time, address, etc.)

    #update delivery status
    def update_status(self, new_status):
        """
        Updates the delivery status of the package.
        This function modifies the `status` attribute of a `Package` object to reflect
        its current state in the delivery process.

        Args:
            new_status (PackageStatus): The new status of the package. Expected values
                                        are from the `PackageStatus` enum.
        Returns:
            None: The function updates the status in place.
        """
        self.status = new_status

    #update departure time
    def update_departure_time(self, departure_time):
        """
        Updates the departure time of the package.
        This function sets the `departure_time` attribute to track when the package
        leaves the hub for delivery.

        Args:
            departure_time (datetime): The timestamp indicating when the package
                                       departs on a truck.
        Returns:
            None: The function updates the departure time in place.
        """
        self.departure_time = departure_time

    #update delivery time (expected)
    def update_delivery_time(self, delivery_time):
        """
        Updates the delivery time of the package.
        This function records the actual delivery time when the package is delivered.
        Args:
            delivery_time (datetime): The timestamp indicating when the package
                                      was delivered.
        Returns:
            None: The function updates the delivery time in place.
        """
        self.delivery_time = delivery_time

    #update street address & Print confirmation to console
    def update_address(self, new_address, new_city = None, new_state = None, new_zip=None):
        """
        Updates the delivery address of the package.
        This function allows modification of the package's address details, including
        the street address, city, state, and ZIP code. If optional parameters are
        provided, they will be updated as well.

        Args:
            new_address (str): The new street address for the package.
            new_city (str, optional): The new city for the package. Defaults to None.
            new_state (str, optional): The new state for the package. Defaults to None.
            new_zip (str, optional): The new ZIP code for the package. Defaults to None.
        Returns:
            None: The function updates the package's address attributes in place.
        """
        logging.info(f"Address update: Package {self.package_id} now has address {new_address} - was {self.address}")
        self.address = new_address
        if new_city:
            self.city = new_city
        if new_zip:
            self.zip_code = new_zip



    #METHODS TO RETRIEVE INFO FROM HASH TABLE OR RESET TABLE

    #pull a list of all packages belonging to a particular truck as truck manifest
    @staticmethod
    def get_packages_by_truck(hash_table, truck_id):
        """
        Retrieves a list of all packages assigned to a specific truck.
        This function searches the hash table for all packages that are assigned
        to a given truck and returns them as a list.

        Args:
            hash_table (HashTable): The hash table storing package data.
            truck_id (int): The ID of the truck for which to retrieve packages.
        Returns:
            list: A list of Package objects assigned to the specified truck.
        """
        return [pkg for bucket in hash_table.table for key, pkg in bucket if pkg.truck == truck_id]

    #define way to clear all info upon reset at start of new day
    @staticmethod
    def reset_hash_table(hash_table):
        """
        Clears all data from the hash table, resetting it for a new delivery day.
        This function reinitializes the hash table by clearing all stored packages,
        resetting its size, and preparing it for new package entries.

        Args:
            hash_table (HashTable): The hash table storing package data.
        Returns:
            None: Modifies the hash table in place.
        """
        hash_table.table = [[] for _ in range(hash_table.capacity)]
        hash_table.size = 0
        hash_table.longest_bucket = 0


    #print human-readable package data when hash table prints
    def __str__(self):
        """
        Returns a human-readable string representation of the package.
        This function provides a formatted string containing the package's
        essential details, including its status, deadlines, delivery information,
        assigned truck, departure time, and delivery address.

        Args:
            None
        Returns:
            str: A formatted string displaying the package's key attributes.
        """
        return (f"Package {self.package_id}: {self.status} | "
            f"Deadline: {self.deadline}, Expected delivery: {self.delivery_time} | "
            f"Truck: {self.truck}, Left hub: {self.departure_time} | "
            f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}")