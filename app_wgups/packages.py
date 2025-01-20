#this class creates Package objects

#define Packages class
class Package:
    #define class object variables
    def __init__(self, package_id, address, city, zip_code, deadline, weight, notes=""):
        self.package_id = package_id  # Unique ID for the package, key in hash table
        self.address = address  # Delivery address
        self.city = city  # Delivery city
        self.zip = zip  # Delivery ZIP code
        self.deadline = deadline  # Delivery deadline
        self.weight = weight  # Weight in kg
        self.notes = notes  # Special delivery notes (optional)
        self.status = "At Hub"  # Default status
        self.delivery_time = None  # Time of delivery (default: not delivered)
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