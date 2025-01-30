#identifying info: Student ID 010899261
#Main program execution happens here: orchestration and user interaction


#Testing Imports - do we need these?
from app_wgups.distance_matrix import load_distance_data
from app_wgups.truck import Truck
from app_wugps.package import Package
from app.hash_table import HashTable()

# Path to the CSV file
csv_path = "data/distance_matrix.csv"
# Load the distances matrix for use by NN algo
distances = load_distance_data(csv_path)

#LOAD PACKAGE DATA, THEN LOAD TRUCKS WITH PACKAGES
package_hash = HashTable()  # Create a new hash table
Package.load_package_data("data/packages_data.csv", package_hash)  # Load fresh data

#create trucks with package lists
truck1 = Truck(1, "09:05")
truck1.load_package(package_hash)

truck2 = Truck(2, "08:00")
truck2.load_package(package_hash)

truck3 = Truck(3, 15:00)  #fix this time
truck3.load_package(package_hash)




total_fleet_travel_distance = truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled


# call function to run routing algo to determine manifest for each truck +
     #simulate the truck's entire route
     #update delivery times in the Packages objects (hash table)
     #track total mileage driven for each truck + all trucks together


#user interface logic
#CLI interface

#user input handling  lookup package status & times, view total truck miles, exit

#lookup all package statuses & print to console all delivery status & times
#get user input - current time of query
#output full list, color coded - HELPER FUNCTIONS?

#lookup one package status by ID and print to console its delivery status and time
#output one package color coded

#lookup manifest of single truck, based on particular time
#output whole truck manifest color coded, label at top "as of ..." time

#OPTIONAL: call reset function to clear all data and load fresh data (.csv)

#exit program


