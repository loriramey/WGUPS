import unittest

from app_wgups.distance_matrix import load_distance_data


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

if __name__ == "__main__":
    # Path to the CSV file
    csv_path = "data/distance_matrix.csv"

    # Load the distances
    distances = load_distance_data(csv_path)

    # Print a few entries to verify
    print(distances["300 State Street"]["10 Main Street"])  # Replace with actual addresses
    print(distances["10 Main Street"]["300 State Street"])  # Should be symmetric
