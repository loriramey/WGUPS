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

    #helper function for getting user inputs
    def get_valid_package_id():
        """Prompt the user for a valid package ID and return an integer or None."""
        package_id = input("\nEnter Package ID#: ").strip()
        if not package_id.isdigit():
            print("ERROR: Package ID must be a number.")
            return None
        return int(package_id)

    def get_valid_time():
        """Prompt the user for a valid time input and return a parsed datetime object or None."""
        check_time = input("Enter time to check in 24-hour format, HH:MM: ").strip()
        parsed_time = parse_time(check_time)  # Convert to datetime
        if parsed_time is None:
            print("ERROR: Invalid time format. Use HH:MM (24-hour).")
            return None
        return parsed_time

    # 🖨️ Option 1: Print single package status
    def print_single_package():
        package_id = get_valid_package_id()  # Use helper function
        if package_id is None:
            return

        parsed_time = get_valid_time()  # Use helper function
        if parsed_time is None:
            return

        lookup_and_print_package_by_ID(package_id, package_hash, parsed_time)

    # 🖨️ Option 2: Print all package statuses
    def print_all_packages():
        parsed_time = get_valid_time()
        if parsed_time is None:
            return
        display_all_package_statuses(package_hash, trucks, parsed_time)

    # 🖨️ Option 3: Print end-of-day status
    def print_eod_status():
        print("\nEOD Status of all Packages:\n")
        display_all_package_statuses(package_hash, trucks, "18:00")

    # 🚪 Option 4: Exit the program
    def exit_program():
        print("\nExiting program. Have an awesome day!\n")
        return False

    # 📋 Menu dictionary mapping options to functions
    menu_options = {
        "1": print_single_package,
        "2": print_all_packages,
        "3": print_eod_status,
        "4": exit_program
    }

    # 🖥️ Print the menu in a loop
    while True:
        print("\n**********************************************")
        print("WELCOME TO THE WGUPS PACKAGE MANAGEMENT SYSTEM")
        print("**********************************************")
        print("1. Print a Single Package Status (Input a Time)")
        print("2. Print All Package Statuses and Truck Mileage (Input a Time)")
        print("3. Print All Package Statuses at EOD")
        print("4. Exit the Program")
        print("**********************************************\n")

        print("Enter your choice: ", end="", flush=True)
        choice = input().strip()

        if choice in menu_options.keys():
            if menu_options[choice]() is False:
                break
        else:
            print("\nX Invalid choice. Please try again.\n")


#helper function to turn user input clock time into a datetime object
def parse_time(user_input):
    """Converts a user-input time string into a datetime object."""
    try:
        return datetime.strptime(user_input, "%H:%M")
    except ValueError:
        print("X ERROR: Invalid time format. Please enter a valid time in HH:MM (24-hour).")
        return None


#helper function for determining package delivery status
def get_package_status_at_time(package, parsed_time):

    if package.departure_time and parsed_time < package.departure_time:
        status = "AT HUB"
    elif package.delivery_time and parsed_time >= package.delivery_time:
        status = "DELIVERED"
    else:
        status = "EN ROUTE"

    return status


#for Task 2 diretions part B: LOOKUP FUNCTION by PACKAGE ID
#helper function - lookup single package by id
def lookup_and_print_package_by_ID(package_id, hash_table, parsed_time):
    print(f"🔍 DEBUG: Looking up package {package_id}")  # New debug message

    package = hash_table.lookup(int(package_id))
    if not package:
        return

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
    print(f"\nDelivery Full Address: {address}, {package.city}, {package.state}, {package.zip_code}")
    print(f"\nDelivery by Truck: {package.truck} |  Package Weight: {package.weight}")
    print(f"\nDelivery Deadline: {package.deadline.strftime('%H:%M') if package.deadline else 'EOD'}")
    print(f"\nDelivery Time: {package.delivery_time.strftime('%H:%M') if package.delivery_time else 'In Transit'}")
    print("------------------------------------------------\n")


#helper function - lookup all packages by time and return status + time, and mileage for all trucks
def display_all_package_statuses(hash_table, trucks, check_time):

    #validate whether check_time is already a date-time object or a string
    if isinstance(check_time, str):
        parsed_time = parse_time(check_time)
    else:
        parsed_time = check_time

    print("\nPackage Statuses at", parsed_time.strftime("%H:%M"), "\n")
    print("-----------------------------------------------")

    total_miles = sum(truck.distance_traveled for truck in trucks)
    package_status_list = []

    for bucket in hash_table.table:
        for _, pkg in bucket:
            status = get_package_status_at_time(pkg, parsed_time)
            address = "300 State St (Incorrect)" if pkg.package_id == 9 and parsed_time < datetime.strptime("10:20","%H:%M") else pkg.address
            if status == "DELIVERED":
                delivery_time = pkg.delivery_time.strftime('%H:%M')
                delivery_time_label = "Delivered"
            else:
                delivery_time = pkg.deadline.strftime('%H:%M')
                delivery_time_label = "Anticipated Delivery"
            truck_number = pkg.truck
            status_colored = colorize_output(status)

            package_status_list.append((
                pkg.package_id,
                f"Package {pkg.package_id}: {status_colored} on Truck {truck_number}; {delivery_time_label}: {delivery_time}"
            ))

    package_status_list.sort(key=lambda x: x[0] )

    for _, package_info in package_status_list:
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

