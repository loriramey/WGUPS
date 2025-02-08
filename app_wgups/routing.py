#this Nearest Neighbor algorithm determines truck route for deliveries (delivery graphs)
from datetime import time
from app_wgups.distance_matrix import get_distance
import logging

class NearestNeighbor:
    def __init__(self, truck, distance_matrix):
        self.truck = truck
        self.distance_matrix = distance_matrix
        self.optimized_manifest = []

    #algorithm logic and implementation
    def calculate_NN_route(self, truck):

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

