import unittest
import sys

sys.path.append('../')
from read_grindstone_csv import ReadGrindstoneCSV

class ReadGrindstoneCSVTest(unittest.TestCase):
    """ Tests the ReadGrindstoneCSV  class"""
    def test_invalid_filepath(self):
        """ Tests initializing with invalid filepath"""
        read_file = ReadGrindstoneCSV("events.csv")
        self.assertFalse(read_file.is_valid)

    def test_invalied_csv(self):
        read_file = ReadGrindstoneCSV("invalid_timeslices.csv")
        self.assertFalse(read_file.is_valid)

    def test_expected_working(self):
        read_file = ReadGrindstoneCSV("test.csv")
        self.assertTrue(read_file.is_valid)
        cal = read_file.get_calendar()
        self.assertFalse(cal is None)
