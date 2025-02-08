#nested dictionary structure to hold WGU Distances data from provided.csv
#Sources for code: Python 3.9.21 documentation found at https://docs.python.org/3.9/index.html
#and W3Schools for data types found at https://www.w3schools.com/python/python_tuples.asp

import csv
from typing import Dict, List, Tuple

# load data from provided Distance Matrix .csv file (stored in data folder)
def load_distance_data(csv_path: str) -> Dict[str, List[Tuple[str, float]]]:

    #return nested dictionary structure with distance matrix as nested dict
    adjacency_matrix = { }   #top-level dict - initialize

    with open(csv_path, mode="r") as csvfile:
        reader = csv.reader(csvfile)

        raw_headers = next(reader)[1: ]  #first row contains address headers, skip cell A1, skip empty columns
        addresses = list(filter(None, [header.strip() for header in raw_headers]))

        for row in reader:
            if not row or len(row) < 2:   #handle broken data
                continue

            from_address = row[0].strip()  #first column contains from_address headers

            distances = []  #initialize interior dict of str address, float distance pairs

            for i, value in enumerate(row[1:len(addresses)+1]):  #iterate & fill dict from .csv
                if value.strip():
                    to_address = addresses[i]
                distances.append( (to_address, float(value)) )

            adjacency_matrix[from_address] = distances

        return adjacency_matrix

#FUNCTION: retrieve distance between any two addresses
def get_distance(distances, from_address, to_address):

   # Direct lookup
    if from_address in distances:
        for address, distance in distances[from_address]:
            if address == to_address:
                return distance

    #Fallback - we can check to_addresses due to data symmetry & get same info
    if to_address in distances:
        for address, distance in distances[to_address]:
            if address == from_address:
                return distance

    # If both fail, return None (no match found)
    return None
