import unittest
import datetime
import sys

sys.path.append('../')
from grindstone_timeslice import TimeSlice

class TimesliceTest(unittest.TestCase):
    """
    Tests the TimeSlice class
    """

    def test_expected_working(self):
        """ Tests the expected working of a timeslice """

        WORK_ITEM = '1181-ROS QSPI FT'
        START_TIME = '8/16/2021 10:39:16 AM'
        DURATION =  '0:15:32'

        test_ts = TimeSlice(WORK_ITEM, START_TIME, DURATION)

        self.assertTrue(test_ts.work_item == WORK_ITEM, 'Work Item does not match')
        self.assertTrue(test_ts.start == START_TIME, 'Start time is not correct')
        self.assertTrue(test_ts.duration == DURATION)
        self.assertEqual(test_ts.get_duration(), 932)

        expected_date = datetime.date(2021, 8, 16)
        self.assertEqual(test_ts.day_date, expected_date, 'Date does not match')
        self.assertEqual(test_ts.get_date(), expected_date, 'Date does not match')
