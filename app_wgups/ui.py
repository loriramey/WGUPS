#functions related to running the CLI UI for end users

from app_wgups.distance_matrix import load_distance_data, get_distance
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.status import PackageStatus
from app_wgups.truck import Truck

#helper function: color code the results (red, yellow, green) for package status

#helper function - get results from Packages and print to screen ?

#helper function - get results from Trucks (manifest of each truck) and print to screen ?

#helper function - load data from files instead of hardcoding into program

#helper function - reset all data to start a new day
#clear hash table and truck manifests
#run the load functions to pull in new material from the data folder

#helper function - exit (do I need this?)


#POSSIBLE CODE TO HANDLE LOOKUPS BY TIME
def get_package_status_at_time(hash_table, check_time):
    """ Returns a list of package statuses as they would be at a given time. """
    package_statuses = []

    for bucket in hash_table.table:
        for _, package in bucket:
            if package.departure_time and check_time < package.departure_time:
                status = "AT HUB"
            elif package.delivery_time and check_time >= package.delivery_time:
                status = "DELIVERED"
            else:
                status = "EN ROUTE"

            package_statuses.append((package.package_id, status, package.address))

    return package_statuses

#UI needs to be able to accept a time input and output datetime obj

#Handle package 9
if package.package_id == 9 and check_time < datetime.strptime("10:20", "%H:%M"):
    address = "300 State St (Incorrect)"
else:
    address = package.address