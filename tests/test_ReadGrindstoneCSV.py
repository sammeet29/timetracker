import unittest
import datetime
import sys

sys.path.append('../')
from read_grindstone_csv import Read_grindstone_csv

class read_grindstone_csv(unittest.TestCase):
    def test_expected_working(self):
        read_file = Read_grindstone_csv()
        self.assertTrue(read_file.is_valid())


if __name__ == "__main__":
    unittest.main()
