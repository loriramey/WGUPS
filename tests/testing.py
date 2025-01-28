import unittest

from app_wgups.distance_matrix import load_distance_data


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


#testing code for the adjacency matrix - how we printed it and tested it.

if __name__ == "__main__":
    # Path to the CSV file
    csv_path = "/Users/loriramey/PycharmProjects/WGUPSapp/data/distance_matrix.csv"

    # Load the distances
    try:
        distances = load_distance_data(csv_path)

        # Print the adjacency matrix for verification
        for from_address, pairs in distances.items():
            print(f"{from_address}: {pairs}")

        print(get_distance(distances, "hub", "1060 Dalton Ave S"))  # Should print 7.2
        print(get_distance(distances, "1060 Dalton Ave S", "hub"))  # Should print 7.2 (symmetric test)
        print(get_distance(distances, "hub", "nonexistent address"))  # Should print None


    except Exception as e:
        print(f"Error: {e}")