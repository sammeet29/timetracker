import unittest
import datetime
from read_grindstone_csv import Time_slice

class Time_slice_test(unittest.TestCase):


    def test_expected_working(self):
        WORK_ITEM = '1181-ROS QSPI FT'
        START_TIME = '8/16/2021 10:39:16 AM'
        DURATION =  '0:15:32'

        tc = Time_slice(WORK_ITEM, START_TIME, DURATION)

        self.assertTrue(tc.work_item == WORK_ITEM, 'Work Item does not match')
        self.assertTrue(tc.start == START_TIME, 'Start time is not correct')
        self.assertTrue(tc.duration == DURATION)

        expected_date = datetime.date(2021, 8, 16)
        self.assertEqual(tc.day_date, expected_date, 'Date does not match')
        self.assertEqual(tc.get_date(), expected_date, 'Date does not match')

if __name__ == "__main__":
    unittest.main()
