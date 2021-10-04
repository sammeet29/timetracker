import unittest
import datetime
import sys

sys.path.append('../')
from read_grindstone_csv import Read_grindstone_csv

class read_grindstone_csv(unittest.TestCase):
    def test_invalid_filepath(self):
        read_file = Read_grindstone_csv("events.csv")
        self.assertFalse(read_file.is_valid)

    def test_invalied_csv(self):
        read_file = Read_grindstone_csv("invalid_timeslices.csv")
        self.assertFalse(read_file.is_valid)

    def test_valid_filepath(self):
        read_file = Read_grindstone_csv("test.csv")
        self.assertTrue(read_file.is_valid)
