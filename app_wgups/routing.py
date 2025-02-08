#this Nearest Neighbor algorithm determines truck route for deliveries (delivery graphs)
#I wrote the pseudocode for this for task 1; sources are listed in that paper. Here is just execution.

from datetime import time
from app_wgups.distance_matrix import get_distance
import logging

class NearestNeighbor:
    def __init__(self, truck, distance_matrix):
        """
        Initializes the Nearest Neighbor algorithm for route optimization.
        This constructor sets up the Nearest Neighbor algorithm, which is used
        to determine an optimized delivery route for a given truck based on
        the provided distance matrix.

        Args:
            truck (Truck): The truck object for which the route is being optimized.
            distance_matrix (dict): A dictionary containing distance data between locations.
        Attributes:
            truck (Truck): The truck assigned to this route optimization.
            distance_matrix (dict): The distance matrix used for calculating routes.
            optimized_manifest (list): A list that stores the optimized package delivery order.
        Returns:
            None
        """
        self.truck = truck
        self.distance_matrix = distance_matrix
        self.optimized_manifest = []


    #algorithm logic and implementation
    def calculate_NN_route(self, truck):
        """
        Computes the optimized delivery route using the Nearest Neighbor algorithm.

        This function determines the most efficient route for the given truck by selecting
        the nearest package destination at each step. It prioritizes delivery deadlines
        when determining the next stop.

        Args:
            truck (Truck): The truck object whose route is being optimized.

        Returns:
            list: An ordered list of Package objects representing the optimized delivery sequence.
        """
    
        remaining_packages = set(truck.manifest[:])  #list of unvisited vertices
        current_vertex = "hub"    #current vertex for comparison

        #Look for the shortest edge that connects current vertex to an unvisited vertex:
        while remaining_packages:
            #prioritize delivery deadlines while searching for nearest vertex
            closest_package = min(
                remaining_packages,
                key=lambda pkg: (
                    get_distance(self.distance_matrix, current_vertex, pkg.address) or float("inf"),
                    pkg.deadline  #sort distance, then check for deadlines
                )
            )
            #check that distance has been calculated
            distance = get_distance(self.distance_matrix, current_vertex, closest_package.address)
            if distance is None:
                logging.warning(f"WARNING: Distance lookup failed for {current_vertex} → {closest_package.address} for {closest_package.package_id}")
                break    #prevents infinite loop

            # update all variables, move package from unvisited to visited vertices list
            self.optimized_manifest.append(closest_package)
            remaining_packages.remove(closest_package)
            current_vertex = closest_package.address #store this as the next starting place for check_distance

        return self.optimized_manifest

