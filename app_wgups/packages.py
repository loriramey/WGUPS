#this class creates Package objects and stores them in a hash table

from app_wgups.status import PackageStatus

#define Packages class to create Package objects
class Package:
    #define class object variables
    def __init__(self, package_id, address, city, zip_code, deadline, weight, notes=""):
        self.package_id = package_id  # Unique ID for the package, key in hash table
        self.address = address  # Delivery address
        self.city = city  # Delivery city
        self.zip = zip_code  # Delivery ZIP code
        self.deadline = deadline  # Delivery deadline
        self.weight = weight  # Weight in kg
        self.notes = notes  # Special delivery notes (optional)

        #additional class variables set by program
        self.status = PackageStatus.AT_HUB  # Default status using enum
        self.departure_time = None #Time package left the hub on a truck, default None
        self.delivery_time = None  #Time of delivery (default: not delivered), default None
        self.truck = truck #assigned truck number

    # define method to update attributes (status, delivery time, address, etc.)
    def update_status(self, status, delivery_time):
        #Update the delivery status and time for the package.
        self.status = status
        if delivery_time:
            self.delivery_time = delivery_time

    def __str__(self):
        #Return a human-readable version of the package info
        return (f"Package {self.package_id}: {self.status} - "
                f"Deadline: {self.deadline}, " f"Expected delivery time: {self.delivery_time}"
                f"Address: {self.address}, {self.city}, {self.zip_code}")


#need more methods
#define way to clear all info upon reset