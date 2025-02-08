#nested dictionary structure to hold WGU Distances data from provided.csv
#Sources for code: Python 3.9.21 documentation found at https://docs.python.org/3.9/index.html
#and W3Schools for data types found at https://www.w3schools.com/python/python_tuples.asp

import csv
from typing import Dict, List, Tuple

# load data from provided Distance Matrix .csv file (stored in data folder)
def load_distance_data(csv_path: str) -> Dict[str, List[Tuple[str, float]]]:
    """
    Loads a distance matrix from a CSV file and returns it as a nested dictionary.
    The function reads a CSV file where the first row contains address headers,
    and subsequent rows contain distances between locations. It returns an adjacency
    matrix, where each key is a "from_address" and its value is a list of tuples
    containing ("to_address", distance).

    Args:
        csv_path (str): The file path to the CSV containing the distance matrix.
    Returns:
        Adjacency Matrix - Dict[str, List[Tuple[str, float]]]:
        A dictionary where keys are addresses and values are lists of (destination_address, distance) tuples.
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If there are invalid or missing distance values in the CSV.
    """
    
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

#Fretrieve distance between any two addresses
def get_distance(distances, from_address, to_address):
    """
    Retrieves the distance between two addresses from a pre-loaded distance matrix.
    This function first attempts to find the direct distance from `from_address`
    to `to_address`. If no direct match is found, it checks the `to_address` entry,
    leveraging data symmetry (i.e., distance from A → B is the same as B → A).

    Args:
        distances (dict): A nested dictionary structure where each key is a `from_address`,
                          and its value is a list of tuples containing `(to_address, distance)`.
        from_address (str): The starting address.
        to_address (str): The destination address.
    Returns:
        float or None: The distance in miles if a match is found; otherwise, returns None.
    """
    
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
