#this class creates Truck objects and data storage for truck manifests, delivery graphs
#sources used when building this code: Python datetime documentation at https://docs.python.org/3.9/library/datetime.html?highlight=time#module-datetime


from app_wgups.distance_matrix import load_distance_data
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
import app_wgups.distance_matrix
from datetime import datetime

from app_wgups.status import PackageStatus
from datetime import datetime, timedelta


class Truck:
    #define class object variables
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.capacity = 16
        self.speed = 18.0  #mph
        self.distance_traveled = 0.0
        self.departure_time = None
        self.current_location = "hub"
        self.manifest = []

        #for testing
        self.delivery_log = []

    #method to load packages onto the truck - for each truck
    def load_package(self, package_hash, departure_time):
        delivery_list = Package.get_packages_by_truck(package_hash, self.truck_id)

        if len(delivery_list) > self.capacity:
            raise ValueError(
                f"🚨 Truck {self.truck_id} overloaded! Capacity is {self.capacity}, "
                f" but {len(delivery_list)} packages were assigned.")

        self.manifest = delivery_list

        #update status of all packages to EN_ROUTE once truck departs
        self.departure_time = departure_time
        # Mark all packages in the manifest as 'EN_ROUTE'
        for package in self.manifest:
            package.update_status(PackageStatus.EN_ROUTE)
            package.update_departure_time(departure_time)

        #FOR TESTING DELETE LATER
        print(f"🚛 Truck {self.truck_id} is scheduled to leave at {self.departure_time}.")

        # FOR TESTING - REMOVE LATER
        # Print confirmation
        print(f"\n🚛 Truck {self.truck_id} loaded with {len(self.manifest)} packages.\n")

        # Print each package's details
        print("📦 Truck Manifest:")
        for pkg in self.manifest:
            print(
                f" - Package {pkg.package_id}: {pkg.address}, {pkg.city}, {pkg.state}, {pkg.zip_code}, Deadline: {pkg.deadline}")
        #END TESTING

        return self.manifest

'''
    #method to determine best route for delivery
    def calculate_delivery_route(self, matrix):
        csv_path = "data/distance_matrix.csv"
        distance_table = load_distance_data(csv_path)
        route = []
        
        #STUB - finish after writing NN algo
        #do stuff to the truck's manifest
        #return it as a new list of vertices
        
        self.manifest = route
        return self.manifest
'''

    # method to update truck's location and total travel distance as it moves
    def deliver_package(self, package, delivery_time):
        package.update_status(PackageStatus.DELIVERED)
        package.update_delivery_time(delivery_time)
        self.delivery_log.append((package.package_id, delivery_time))
        self.manifest.remove(package)

    def move_truck(self, new_location, distance):
        self.distance_traveled += distance
        self.current_location = new_location



#FOR TESTING TRUCK CLASS
package_hash = HashTable()
Package.load_package_data("/Users/loriramey/PycharmProjects/WGUPSapp/data/packages_data.csv", package_hash)

truck1 = Truck(1, "08:00")
truck1.load_package(package_hash)

