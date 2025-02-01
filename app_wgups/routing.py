#this Nearest Neighbor algorithm determines truck route for deliveries (delivery graphs)
from datetime import datetime
from app_wgups.distance_matrix import get_distance
from app_wgups.package import Package
from app_wgups.truck import Truck

class NearestNeighbor:
    def __init__(self, truck, distance_matrix):
        self.truck = truck
        self.distance_matrix = distance_matrix
        self.incoming_manifest = []
        self.optimized_manifest = []
        self.total_miles = 0.0

    #algorithm logic and implementation
    def calculate_NN_route(self, truck):

        self.incoming_manifest = truck.manifest[:]

        #IDENTIFY HIGH PRIORITY PACKAGES
        urgent_packages = [pkg for pkg in self.incoming_manifest if pkg.deadline < datetime.time(10, 30)]

        #SET STARTING VERTEX TO HUB, INITIALIZE LOOP VARIABLES
        current_vertex = "hub"
        next_stop = None

        #Look for the shortest edge that connects C-V to an unvisited vertex:
        i=0
        while self.incoming_manifest:
            nearest_pkg = None
            min_distance = 100.0  #initialize to high value for each pass

            #loop through truck manifest to find nearest neighbor, but consider priority deadlines
            for pkg in self.incoming_manifest:
                check_distance = get_distance(self.distance_matrix, current_vertex, pkg.address)

                if check_distance < min_distance:   #check for nearest neighbor, store if shorter than current minimum
                    nearest_pkg = pkg
                    min_distance = check_distance
                elif check_distance == min_distance:  # how to handle race btw 2 packages, same distance = priority tiebreaker
                    if pkg in urgent_packages:   #check delivery priority time
                        nearest_pkg = pkg
                        min_distance = check_distance

            if nearest_pkg:  #update, move package from unvisited to visited vertices list
                self.optimized_manifest.append(nearest_pkg)
                self.incoming_manifest.remove(nearest_pkg)

                current_vertex = nearest_pkg.address #store this as the next starting place for check_distance

        return self.optimized_manifest

