import os
from app_wgups.package import Package
from app_wgups.hash_table import HashTable

# Fix file path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get tests/ folder
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Move to WGUPSapp/
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CSV_FILE_PATH = os.path.join(DATA_DIR, "packages_data.csv")

# Initialize hash table
hash_table = HashTable()

# Load packages
Package.load_package_data(CSV_FILE_PATH, hash_table)

# Verify packages loaded
print("Number of Packages Loaded:", hash_table.size)

# Pick a random package to check (adjust as needed)
sample_package = hash_table.lookup(9)  # Example: Check Package 9
if sample_package:
    print(f"Package {sample_package.package_id} | Address: {sample_package.address} | Deadline: {sample_package.deadline}")
else:
    print("Error: Package 9 not found")