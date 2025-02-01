import os

# Get absolute path to the project's root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets current file's directory (tests/)
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Go up one level to WGUPSapp
DATA_DIR = os.path.join(PROJECT_ROOT, "data")  # Point to the data folder

CSV_FILE_PATH = os.path.join(DATA_DIR, "packages_data.csv")  # Use correct file name

print("Absolute CSV Path:", CSV_FILE_PATH)
print("File Exists:", os.path.exists(CSV_FILE_PATH))