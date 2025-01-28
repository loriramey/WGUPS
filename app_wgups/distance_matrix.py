#nested dictionary structure to hold WGU Distances data from .csv
#Sources for code: Python 3.9.21 documentation found at https://docs.python.org/3.9/index.html

import csv
from typing import Dict, Any

# load data from provided Distance Matrix .csv file (stored in data folder)
def load_distance_data(csv_path):

    #return nested dictionary structure with distance matrix as nested dict
    distances: Dict[str, Dict[str, float]] = {}   #top-level dict - initialize

    #for testing file paths
    print(f"Attempting to load file: {csv_path}")

    with open(csv_path, mode="r") as csvfile:
        reader = csv.reader(csvfile)

        addresses = [address.strip() for address in next(reader)]  #first row contains address headers

        # FOR TESTING - DELETE
        print("Addresses (header row):", addresses)

        for row in reader:
            from_address = row[0].strip() #first column contains address headers
            distances[from_address] = {}   #nested dict - initialize

            #Iterate over distances and build nested dict entries (distances for each address)
            for col, distance in enumerate(row[1:], start=1):
                to_address = addresses[col].strip()

                #FOR TESTING - DELETE
                print(f"Processing from_address: {from_address}")
                print(f"Row data: {row[1:]}")

                #allows for empty spaces in .csv to not break the code
                if distance.strip():
                    distances[from_address][to_address] = {"address": to_address, "distance": float(distance)}  #populate dict
                else:
                    distances[from_address][to_address] = {"address": to_address, "distance": 0.0}  #defaults to 0.0 hub

    return distances

#
def get_distance(distances, from_address, to_address):

    #direct lookup

    # Direct lookup
    if from_address in distances and to_address in distances[from_address]:
        return distances[from_address][to_address]["distance"]

    # Fallback if direct lookup fails
    if to_address in distances and from_address in distances[to_address]:
        return distances[to_address][from_address]["distance"]

    # If both fail, return None
    return None



if __name__ == "__main__":
    # Path to the CSV file
    csv_path = "/Users/loriramey/PycharmProjects/WGUPSapp/data/distance_matrix.csv"

    # Load the distances
    distances = load_distance_data(csv_path)

    # Print a few entries to verify
    print(distances["300 State Street"]["10 Main Street"])  # Replace with actual addresses
    print(distances["10 Main Street"]["300 State Street"])  # Should be symmetric



