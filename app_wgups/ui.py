#USER INTERFACE: functions related to running the CLI UI for end users

from datetime import datetime
import sys

from app_wgups import package
from app_wgups.distance_matrix import load_distance_data
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.status import PackageStatus
from app_wgups.truck import Truck

#INITIALIZE GLOBAL VARIABLES
package_hash = HashTable()
distance_matrix = None
trucks = []


#UI INTERFACE CODE - basic CLI interface with dictionary of options
def user_interface(package_hash, trucks):

    #functions for each option in the menu
    def print_single_package():
        package_id = input("\nEnter Package ID#:").strip()
        if not package_id.isdigit():  #checks for valid ID number format (integer)
            print("Invalid input. Package ID must be a number.")
        package_id = int(package_id)

        check_time = input("Enter time to check in 24-hour format, HH:MM: ").strip()
        parsed_time = parse_time(check_time)  #check for valid time format
        if parsed_time is None:
            return

        lookup_and_print_package_by_ID(package_id, package_hash, check_time)

    def print_all_packages():
        check_time = input("\nEnter time in 24-hour format, HH:MM: ").strip()
        parsed_time = parse_time(check_time) #checks that tim is valid format
        if parsed_time is None:
            return

        display_all_package_statuses(package_hash, trucks, check_time)

    def print_eod_status():
        print("\nEOD Status of all Packages:\n")
        display_all_package_statuses(package_hash, trucks, "18:00")

    def exit_program():
        print("\nExiting program. Have an awesome day!\n")
        return False


    #dictionary to map user input to options
    menu_options = {
        "1": print_single_package,
        "2": print_all_packages,
        "3": print_eod_status,
        "4": exit_program
    }

    #print menu options to screen
    while True:
        print("\n**********************************************")
        print("WELCOME TO THE WGUPS PACKAGE MANAGEMENT SYSTEM")
        print("**********************************************\n")
        print("1. Print a Single Package Status (Input a Time)")
        print("2. Print All Package Statuses and Truck Mileage (Input a Time)")
        print("3. Print All Package Statuses at EOD")
        print("4. Exit the Program")
        print("\n**********************************************\n")

        print("Enter your choice: ", end="", flush=True)
        choice = input().strip()

        if choice in menu_options.keys():
            if menu_options[choice]() is False:
                break
        else:
            print("\nInvalid choice. Please try again.\n")


#helper function - parse times from UI into datetime object
def parse_time(user_input):
    if isinstance(user_input, datetime): #make sure this input is not already a datetime object
        try:
            return datetime.strptime(user_input, "%H:%M")
        except ValueError:
            print("Invalid time format. Please enter a time using a four-digit 24-hour format.\n")
            print("For example, enter 09:00 for 9 am or 13:30 for 1:30 pm.")
            return None


#helper function for determining package delivery status
def get_package_status_at_time(package, check_time):
    parsed_time = parse_time(check_time)

    if package.departure_time and parsed_time < package.departure_time:
        status = "AT HUB"
    elif package.delivery_time and parsed_time >= package.delivery_time:
        status = "DELIVERED"
    else:
        status = "EN ROUTE"

    return status


#for Task 2 diretions part B: LOOKUP FUNCTION by PACKAGE ID
#helper function - lookup single package by id
def lookup_and_print_package_by_ID(package_id, hash_table, check_time):

    package = hash_table.lookup(int(package_id))
    parsed_time = parse_time(check_time)

    if parsed_time is None or not package:  #error handling if user inputs invalid time
        print(f"Package with ID {package_id} not found")
        return

    #package9 has wrong address till 10:20am
    status = get_package_status_at_time(package, parsed_time)
    address = "300 State St (Incorrect)" if package.package_id == 9 and parsed_time < datetime.strptime("10:20", "%H:%M") else package.address

    #print to screen
    print(f"\nPackage {package_id} Status at {parsed_time.strftime('%H:%M')}")
    print("------------------------------------------------")
    print(f"Status: {colorize_output(status)}")
    print(f"\nDelivery Full Address: {address}, {package.city}, {package.state}, {package.zip}")
    print(f"\nDelivery by Truck: {package.truck} |  Package Weight: {package.weight}")
    print(f"\nDelivery Deadline: {package.deadline.strftime('%H:%M') if package.deadline else 'EOD'}")
    print(f"\nDelivery Time: {package.delivery_time.strftime('%H:%M') if package.delivery_time else 'In Transit'}")
    print("------------------------------------------------\n")


#helper function - lookup all packages by time and return status + time, and mileage for all trucks
def display_all_package_statuses(hash_table, trucks, check_time):

    parsed_time = parse_time(check_time)
    if parsed_time is None:  # error handling if user inputs invalid time
        return

    print("\nPackage Statuses at", parsed_time.strftime("%H:%M"), "\n")
    print("-----------------------------------------------")

    total_miles = sum(truck.distance for truck in trucks)
    package_status_list = []

    for bucket in hash_table:
        for _, pkg in bucket:
            status = get_package_status_at_time(pkg, parsed_time)
            address = "300 State St (Incorrect)" if pkg.package_id == 9 and parsed_time < datetime.strptime("10:20","%H:%M") else pkg.address
            delivery_time = pkg.delivery_time.strftime('%H:%M') if pkg.delivery_time else "Anticipated: TBD"
            truck_number = pkg.truck
            status_colored = colorize_output(status)

            package_status_list.append(f"Package {pkg.package_id}: {status_colored} on Truck {truck_number}; Delivery Time: {delivery_time}")

    for package_info in sorted(package_status_list):
        print(package_info)

    print("-----------------------------------------------\n")
    print(f"\nTotal Truck Mileage: {total_miles:.2f}")
    print("-----------------------------------------------\n")


#helper function - reset all data to start a new day
def reset_day(package_hash, trucks):
    package_hash.clear()

    for truck in trucks:
        truck.manifest.clear()
        truck.delivery_log.clear()
        truck.distance_traveled = 0.0
        truck.current_location = "hub"
        truck.current_time = None
        truck.return_time = None

    print("System reset; all package and truck data cleared.")


#helper function: color code any results printed to screen based on package status
def colorize_output(status):
    colors = {
        "AT HUB": "\033[91m",  # Red
        "EN ROUTE": "\033[93m",  # Yellow
        "DELIVERED": "\033[92m",  # Green
        "RESET": "\033[0m"  # Reset color formatting
    }
    return f"{colors.get(status, colors['RESET'])}{status}{colors['RESET']}"

