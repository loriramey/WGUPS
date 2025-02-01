#identifying info: Student ID 010899261
#Main program execution happens here: orchestration and user interaction


#Testing Imports - do we need these?
from datetime import datetime, timedelta
import os
import logging

from app_wgups.distance_matrix import load_distance_data, get_distance
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from app_wgups.status import PackageStatus
from app_wgups.truck import Truck
from app_wgups.distance_matrix import load_distance_data
from app_wgups.truck import Truck
from app_wugps.package import Package
from app.hash_table import HashTable


#IMPLEMENT A LOGGING PROCESS TO CATCH ALL ERRORS AND LOGS, PRINT CRITICAL ERRORS TO CONSOLE
logging.basicConfig(
    filename="wgups_debug.log",  # Log file name
    level=logging.DEBUG,  # Capture all debug, info, warning, and error messages
    format="%(asctime)s [%(levelname)s] %(message)s",  # Include timestamp
    filemode="w",  # Overwrite log file on each run (use "a" to append instead)
)
# Create a second handler to print only errors to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)

# Add the handler to the root logger
logging.getLogger().addHandler(console_handler)


#------MAIN PROGRAM LOGIC------------




#OPTIONAL: call reset function to clear all data and load fresh data (.csv)
#exit program
