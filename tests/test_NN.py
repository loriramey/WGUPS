import unittest
from app_wgups.package import Package
from app_wgups.truck import Truck
from app_wgups.routing import NearestNeighbor
from app_wgups.distance_matrix import get_distance
from app_wgups.hash_table import HashTable
import os


class TestNearestNeighbor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up package data, truck, and distance matrix before tests."""
        cls.hash_table = HashTable()

        # Load package data from CSV
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Locate test directory
        DATA_DIR = os.path.join(BASE_DIR, "..", "data")  # Adjust if needed
        CSV_FILE_PATH = os.path.join(DATA_DIR, "packages_data.csv")

        Package.load_package_data(CSV_FILE_PATH, cls.hash_table)

        # Create Truck 2 and assign packages (example)
        cls.truck = Truck(2)
        cls.truck.manifest = Package.get_packages_by_truck(cls.hash_table, 2)

        # Load distance matrix
        cls.distance_matrix = os.path.join(DATA_DIR, "distance_matrix.csv")

    def test_nearest_neighbor_algorithm(self):
        """Test the NN algorithm's package ordering."""
        nn = NearestNeighbor(self.truck, self.distance_matrix)
        optimized_manifest = nn.calculate_NN_route(self.truck)

        # Ensure the same number of packages are in optimized_manifest
        self.assertEqual(len(optimized_manifest), len(self.truck.manifest))

        # Verify that packages were re-ordered
        self.assertNotEqual(self.truck.manifest, optimized_manifest)

        # Check if the first stop is closest to the hub
        hub_address = "hub"
        first_stop = optimized_manifest[0].address
        second_stop = optimized_manifest[1].address
        self.assertLessEqual(
            get_distance(self.distance_matrix, hub_address, first_stop),
            get_distance(self.distance_matrix, hub_address, second_stop)
        )


if __name__ == "__main__":
    unittest.main()