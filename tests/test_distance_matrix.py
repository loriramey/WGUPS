import unittest

from app_wgups.distance_matrix import load_distance_data


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


#testing code for the adjacency matrix - how we printed it and tested it.

if __name__ == "__main__":
    # Path to the CSV file
    csv_path = "/Users/loriramey/PycharmProjects/WGUPSapp/data/distance_matrix.csv"

    # Load the distances
    try:
        distances = load_distance_data(csv_path)

        # Print the adjacency matrix for verification
        for from_address, pairs in distances.items():
            print(f"{from_address}: {pairs}")

        print(get_distance(distances, "hub", "1060 Dalton Ave S"))  # Should print 7.2
        print(get_distance(distances, "1060 Dalton Ave S", "hub"))  # Should print 7.2 (symmetric test)
        print(get_distance(distances, "hub", "nonexistent address"))  # Should print None


    except Exception as e:
        print(f"Error: {e}")






#FOR TESTING HASH TABLE - DELETE LATER
if __name__ == "__main__":
    # Create a new HashTable instance
    hash_table = HashTable(capacity=5)  # Small capacity for testing resize logic

    print("\n🔹 Initial Table:")
    print(hash_table)  # Should print an empty table

    # Test INSERT
    print("\n🔹 Testing Insertions:")
    hash_table.insert(1, "Package A")
    hash_table.insert(2, "Package B")
    hash_table.insert(3, "Package C")
    hash_table.insert(4, "Package D")  # Will test chaining if collision occurs
    hash_table.insert(5, "Package E")
    print(hash_table)  # Verify all insertions worked

    # Test SEARCH (Retrieve)
    print("\n🔹 Testing Search:")
    print(f"Search for key 3: {hash_table.search(3)}")  # Expected: Package C
    print(f"Search for key 99 (non-existent): {hash_table.search(99)}")  # Expected: None

    # Test UPDATE
    print("\n🔹 Testing Update:")
    hash_table.update(2, "Updated Package B")
    print(f"Updated key 2: {hash_table.search(2)}")  # Expected: Updated Package B

    # Test DELETE
    print("\n🔹 Testing Deletion:")
    print(f"Deleting key 4: {hash_table.delete(4)}")  # Expected: True
    print(f"Search for deleted key 4: {hash_table.search(4)}")  # Expected: None
    print(hash_table)  # Verify deletion in printed table

    # Test RESIZE (Insert more elements to trigger resize)
    print("\n🔹 Testing Auto-Resize:")
    for i in range(6, 26):  # Insert more items to trigger resize
        hash_table.insert(i, f"Package {i}")
    print(hash_table)  # Table should have expanded

    # Final check
    print("\n✅ All basic hash table operations tested successfully!")


#TESTING PACKAGE CLASS



# FOR TESTING PURPOSES
print("\n🔹 TESTING PACKAGE METHODS\n")
from app_wgups.hash_table import HashTable
from app_wgups.package import Package

package_hash = HashTable()
Package.load_packages("data/packages_data.csv", package_hash)
print(package_hash)  # Should display all packages
# Retrieve a package by ID
test_package = package_hash.search(1)  # Search for package with ID 1
if test_package:
    print(f"📦 Found Package 1: {test_package}\n")
else:
    print("❌ Package 1 not found.\n")

# Update a package's status
test_package.update_status(PackageStatus.EN_ROUTE)
print(f"📦 Updated Package 1 Status: {test_package.status}\n")

# Update a package's departure time
test_package.update_departure_time("08:30 AM")
print(f"🚚 Package 1 Departure Time: {test_package.departure_time}\n")

# Update a package's delivery time
test_package.update_delivery_time("09:15 AM")
print(f"📍 Package 1 Delivery Time: {test_package.delivery_time}\n")

# Retrieve all packages assigned to a specific truck
truck_id = 2  # Example truck ID
truck_packages = Packages.get_packages_by_truck(package_hash, truck_id)

print(f"🚛 Truck {truck_id} Manifest:")
for pkg in truck_packages:
    print(pkg)

print("\n🔹 TESTING PACKAGE ADDRESS UPDATE\n")

# Fetch the package that we know has an incorrect address (let's say it's Package 9 for this example)
test_package = package_hash.search(9)

if test_package:
    print(f"📦 BEFORE Update: {test_package}\n")

    # Simulate 10:20 AM address correction
    current_time = "10:20 AM"  # Replace with a real-time check in full program
    if current_time >= "10:20 AM":
        test_package.update_address("410 S State St", "Salt Lake City", "84111")

    print(f"📦 AFTER Update: {test_package}\n")
else:
    print("❌ Package not found!")