#testing NN algo

import unittest
from app_wgups.hash_table import HashTable
from app_wgups.package import Package
from datetime import time

class TestPackageData(unittest.TestCase):
    def setUp(self):
        self.hash_table = HashTable()
        Package.load_package_data("package_data.csv", self.hash_table)

    def test_deadline_is_time_object(self):
        """ Ensure all package deadlines are stored as datetime.time """
        for i in range(1, 41):  # Assuming package IDs are 1-40
            package = self.hash_table.search(i)
            self.assertIsInstance(package.deadline, time, f"Package {i} deadline is not a time object")

    def test_deadline_correct_conversion(self):
        """ Ensure specific package deadlines match expected times """
        package_1 = self.hash_table.search(1)
        package_5 = self.hash_table.search(5)

        self.assertEqual(package_1.deadline, time(9, 0), "Package 1 should have deadline 09:00")
        self.assertEqual(package_5.deadline, time(23, 59), "Package 5 should have deadline 23:59 (EOD)")