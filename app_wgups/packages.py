#this class creates Package objects and stores them in a hash table
import csv
from app_wgups.hash_table import HashTable
from app_wgups.status import PackageStatus

#define Packages class to create Package objects
class Packages:
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
                package = Packages(
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


    #define method to pull a list of all packages belonging to a particular truck as truck manifest
    @staticmethod
    def get_packages_by_truck(hash_table, truck_id):
        return [pkg for bucket in hash_table.table for key, pkg in bucket if pkg.truck == truck_id]

#method to retrieve list of packages from the system for UI

#need other method? to retrieve single package object info
#will need to be able to retrieve just one variable from object, like "status" or "delivery time"

#method to call update function from hash table to update individual variables inside a package obj
#example: update the delivery time once it's calculated and store in the package object

#define way to clear all info upon reset at start of new day


    def __str__(self):
        #Return a human-readable version of the package info
        return (f"Package {self.package_id}: {self.status} | "
                f"Deadline: {self.deadline}, Expected delivery: {self.delivery_time} | "
                f"Truck: {self.truck}, Left hub: {self.departure_time} | "
                f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}")


#FOR TESTING DELETE LATER
# FOR TESTING PURPOSES
print("\n TESTING HASH TABLE LOAD\n")
package_hash = HashTable()
Packages.load_package_data("/Users/loriramey/PycharmProjects/WGUPSapp/data/packages_data.csv", package_hash)
print(package_hash)  # Should display all packages

print("\n🔹 TESTING PACKAGE METHODS\n")

# Retrieve a package by ID
test_package = package_hash.search(1)  # Search for package with ID 1
if test_package:
    print(f"📦 Found Package 1: {test_package}\n")
else:
    print("❌ Package 1 not found.\n")

# Update a package's status
test_package.update_status(PackageStatus.EN_ROUTE)
print(f"📦 Updated Package 1 Status: {test_package.status}\n")

# Update a package's departure time
test_package.update_departure_time("08:30 AM")
print(f"🚚 Package 1 Departure Time: {test_package.departure_time}\n")

# Update a package's delivery time
test_package.update_delivery_time("09:15 AM")
print(f"📍 Package 1 Delivery Time: {test_package.delivery_time}\n")

# Retrieve all packages assigned to a specific truck
truck_id = 2  # Example truck ID
truck_packages = Packages.get_packages_by_truck(package_hash, truck_id)

print(f"🚛 Truck {truck_id} Manifest:")
for pkg in truck_packages:
    print(pkg)
