from datetime import datetime

from app_wgups.distance_matrix import load_distance_data
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.truck import Truck  # Ensure this import is correct

# 🚛 **STEP 1: Load Data**
print("\n📦 LOADING PACKAGE DATA & DISTANCE MATRIX...\n")

package_hash = HashTable()
Package.load_package_data("/Users/loriramey/PycharmProjects/WGUPSapp/data/packages_data.csv", package_hash)

distance_matrix = load_distance_data("/Users/loriramey/PycharmProjects/WGUPSapp/data/distance_matrix.csv")

# 🚛 **STEP 2: Initialize & Load Trucks**
truck1 = Truck(1)
truck2 = Truck(2)

truck1.departure_time = datetime.strptime("09:05", "%H:%M")
truck2.departure_time = datetime.strptime("08:00", "%H:%M")

for truck in (truck1, truck2):
    truck.load_package(package_hash, truck.departure_time)

# 🚛 **STEP 3: Simulate Truck 1's Route**
print("\n🚛 TRUCK 1: Simulating Route and Deliveries...\n")
while truck1.manifest:
    truck1.deliver_package(truck1.manifest[0], distance_matrix)

print(f"✅ Truck 1 returned to hub at {truck1.return_time.strftime('%H:%M')}, Total Distance: {truck1.distance_traveled:.2f} miles\n")

# 🚛 **STEP 4: Simulate Truck 2's Route**
print("\n🚛 TRUCK 2: Simulating Route and Deliveries...\n")
while truck2.manifest:
    truck2.deliver_package(truck2.manifest[0], distance_matrix)

print(f"✅ Truck 2 returned to hub at {truck2.return_time.strftime('%H:%M')}, Total Distance: {truck2.distance_traveled:.2f} miles\n")

#new truck 3 tests to handle wrong address package

# 🚛 TRUCK 3: Waiting for Available Truck...
print("\n🚛 TRUCK 3: Preparing to Load and Depart...\n")

# 🚛 STEP 1: Ensure Truck 1 and Truck 2 Have Returned
if truck1.return_time is None:
    truck1.return_to_hub(distance_matrix)
if truck2.return_time is None:
    truck2.return_to_hub(distance_matrix)

# 🚛 STEP 2: Calculate Truck 3 Departure Time
truck3_departure_time = Truck.calculate_truck3_departure(truck1, truck2, distance_matrix)

# 🚛 STEP 3: Initialize Truck 3 & Load Packages
truck3 = Truck(3)
truck3.load_package(package_hash, truck3_departure_time)

# 🚛 STEP 4: Print Truck 3 Manifest Before Address Fix
print("\n📦 TRUCK 3 PACKAGE MANIFEST BEFORE DELIVERY:\n")
for pkg in truck3.manifest:
    print(f"Package {pkg.package_id}: Address - {pkg.address}")

# 🔧 STEP 5: Simulate Address Correction at 10:20 AM
package_9 = package_hash.lookup(9)
package_9.update_address("410 S State St", "Salt Lake City", "UT", "84111")
print(f"\n🔧 UPDATE: Correcting Package 9 Address at 10:20 AM: Now {package_9.address}")

# 🚛 STEP 6: Simulate Truck 3 Deliveries
print("\n🚛 TRUCK 3: Simulating Route and Deliveries...\n")
while truck3.manifest:
    truck3.deliver_package(truck3.manifest[0], distance_matrix)

# ✅ STEP 7: Report Truck 3 Return Time and Total Distance
print(f"\n✅ Truck 3 returned to hub at {truck3.return_time.strftime('%H:%M')}, "
      f"Total Distance: {truck3.distance_traveled:.2f} miles\n")