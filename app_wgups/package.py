#this class creates Package objects and stores them in a hash table
import csv
from app_wgups.hash_table import HashTable
from app_wgups.status import PackageStatus

#define Packages class to create Package objects
class Package:
    #define class object variables
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes="", truck=None):
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
        with open(csv_filepath, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)

            for row in reader:  #read in a package object
                package = Package(
                    package_id=int(row[0]),
                    address=row[1],
                    city=row[2],
                    state=row[3],
                    zip_code=row[4],
                    deadline=row[5],
                    weight=int(row[6]),
                    notes=row[7] if len(row) > 7 else "",
                    truck=int(row[8]) if len(row) > 8 and row[8].strip() else None
                )
                hash_table.insert(package.package_id, package)


    # define methods to update attributes (status, delivery time, address, etc.)

    #update delivery status
    def update_status(self, new_status):
        self.status = new_status

    #update departure time
    def update_departure_time(self, departure_time):
        self.departure_time = departure_time

    #update delivery time (expected)
    def update_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time

    #update street address & Print confirmation to console
    def update_address(self, new_address, new_city = None, new_zip=None):
        print(f"Address update: Package {self.package_id} now has address {new_address} - was {self.address}")
        self.address = new_address
        if new_city:
            self.city = new_city
        if new_zip:
            self.zip_code = new_zip

    #METHODS TO RETRIEVE INFO FROM HASH TABLE OR RESET TABLE
    #pull a list of all packages belonging to a particular truck as truck manifest
    @staticmethod
    def get_packages_by_truck(hash_table, truck_id):
        return [pkg for bucket in hash_table.table for key, pkg in bucket if pkg.truck == truck_id]

    #define way to clear all info upon reset at start of new day
    @staticmethod
    def reset_hash_table(hash_table):
        """ Completely clears all entries from the hash table. """
        hash_table.table = [[] for _ in range(hash_table.capacity)]
        hash_table.size = 0  # Reset count
        hash_table.longest_bucket = 0  # Reset bucket tracking

    #print human-readable package data when hash table prints
    def __str__(self):
        return (f"Package {self.package_id}: {self.status} | "
                f"Deadline: {self.deadline}, Expected delivery: {self.delivery_time} | "
                f"Truck: {self.truck}, Left hub: {self.departure_time} | "
                f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}")
