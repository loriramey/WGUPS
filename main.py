#identifying info: Student ID 010899261
#Main program execution happens here: orchestration and user interaction


#Testing Imports - do we need these?
from app_wgups.distance_matrix import load_distance_data

#ACTUAL IMPORTS

# initialize data structures - hash table for packages
# load hardcoded data: adjacency matrix, package info
     #consider calling helper functions here for future improvements
# call function to load package data, generate package objects, fill hash table

package_hash = HashTable()
Package.load_packages_from_csv("data/packages.csv", package_hash)


# call function to load distance adjacency data
# call function to create truck objects
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


#TESTING
if __name__ == "__main__":
    # Path to the CSV file
    csv_path = "data/distance_matrix.csv"

    # Load the distances
    distances = load_distance_data(csv_path)

    # Print a few entries to verify
    print(distances["300 State Street"]["10 Main Street"])  # Replace with actual addresses
    print(distances["10 Main Street"]["300 State Street"])  # Should be symmetric
