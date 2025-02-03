import unittest
from unittest.mock import patch
from io import StringIO

from datetime import datetime
from app_wgups.distance_matrix import load_distance_data
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.truck import Truck
from app_wgups.ui import user_interface
import os

# 🚛 **STEP 1: Load Data**

# Dynamically set the base directory (assumes "tests" folder is at project root level)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Locate "tests" directory
DATA_DIR = os.path.join(BASE_DIR, "..", "data")  # Move up to project root, then into "data"
CSV_FILE_PATH_PACKAGES = os.path.join(DATA_DIR, "packages_data.csv")
CSV_FILE_PATH_DISTANCES = os.path.join(DATA_DIR, "distance_matrix.csv")

package_hash = HashTable()
Package.load_package_data(CSV_FILE_PATH_PACKAGES, package_hash)

distance_matrix = load_distance_data(CSV_FILE_PATH_DISTANCES)

# 🚛 **STEP 2: Initialize & Load Trucks**
truck1 = Truck(1)
truck2 = Truck(2)

truck1.departure_time = datetime.strptime("09:05", "%H:%M")
truck2.departure_time = datetime.strptime("08:00", "%H:%M")

for truck in (truck1, truck2):
    truck.load_package(package_hash, truck.departure_time)

# 🚛 **STEP 3: Optimize Routes Before Deliveries**
for truck in (truck1, truck2):

    original_manifest = [pkg.package_id for pkg in truck.manifest]  # Track original order
    truck.calculate_delivery_route(distance_matrix)  # Apply NN Algorithm
    optimized_manifest = [pkg.package_id for pkg in truck.manifest]  # Track optimized order

# 🚛 **STEP 4: Simulate Truck 1's Route**
while truck1.manifest:
    truck1.deliver_package(truck1.manifest[0], distance_matrix)

# 🚛 **STEP 5: Simulate Truck 2's Route**
while truck2.manifest:
    truck2.deliver_package(truck2.manifest[0], distance_matrix)


# 🚛 **STEP 6: Truck 3 - Waiting for Available Truck**

# 🚛 Ensure Truck 1 and Truck 2 Have Returned
if truck1.return_time is None:
    truck1.return_to_hub(distance_matrix)
if truck2.return_time is None:
    truck2.return_to_hub(distance_matrix)

# 🚛 Calculate Truck 3 Departure Time
truck3_departure_time = Truck.calculate_truck3_departure(truck1, truck2, distance_matrix)

# 🚛 Initialize Truck 3 & Load Packages
truck3 = Truck(3)
truck3.load_package(package_hash, truck3_departure_time)

# 🚛 Print Truck 3 Manifest Before Address Fix

# 🔧 Fix Package 9 Address at 10:20 AM
package_9 = package_hash.lookup(9)
package_9.update_address("410 S State St", "Salt Lake City", "UT", "84111")

# 🚛 Optimize Truck 3's Route Before Deliveries
truck3.calculate_delivery_route(distance_matrix)

# 🚛 Simulate Truck 3 Deliveries
while truck3.manifest:
    truck3.deliver_package(truck3.manifest[0], distance_matrix)


#-------------------------------
#TESTING THE UI NOW THAT WE HAVE WORKING TRUCKS

class TestUIMenu(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '7', '10:00', '4'])  # Simulate user selecting option 1, then exit (4)
    @patch('sys.stdout', new_callable=StringIO)  # Capture printed output
    def test_menu_selection_valid(self, mock_stdout, mock_input):
        """Test if the UI correctly handles a valid menu selection."""

        user_interface(package_hash, [truck1, truck2, truck3])  # Pass required arguments

        output = mock_stdout.getvalue()  # Capture the printed output

        # Expected output checks
        self.assertIn("1. Print a Single Package Status (Input a Time)", output)
        self.assertIn("2. Print All Package Statuses and Truck Mileage (Input a Time)", output)
        self.assertIn("3. Print All Package Statuses at EOD", output)
        self.assertIn("4. Exit the Program", output)
        self.assertIn("Enter your choice:", output)  # Ensures input prompt was shown
        self.assertIn("Exiting program. Have an awesome day!", output)  # Match actual UI output

    @patch('builtins.input', side_effect=['7', 'a', '4', '4'])  # Invalid choices first, then valid exit
    @patch('sys.stdout', new_callable=StringIO)
    def test_menu_selection_invalid(self, mock_stdout, mock_input):
        """Test if the UI correctly handles invalid menu selections."""

        user_interface(package_hash, [truck1, truck2, truck3])  # Pass required arguments

        output = mock_stdout.getvalue()  # Capture the printed output

        # Expected output checks
        self.assertIn("Invalid choice. Please try again.",
                      output)  # Match the actual message
        self.assertIn("Exiting program. Have an awesome day!", output)  # Confirms clean exit


if __name__ == '__main__':
    unittest.main()