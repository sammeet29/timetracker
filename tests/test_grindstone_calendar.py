import unittest
import sys
import datetime

sys.path.append('../')
from grindstone_calendar import Calendar
from grindstone_timeslice import Time_slice

WORK_ITEM = '1181-ROS QSPI FT'
START_TIME = '8/16/2021 10:39:16 AM'
DURATION =  '0:15:32'

class Calender_test(unittest.TestCase):
    def setUp(self):
        self.cal = Calendar()
        entries = self.cal.get_entries()
        self.assertEqual(0,len(entries))

    def tearDown(self):
        self.cal.clear_entries()

    def test_single_entry(self):
        tc = Time_slice(WORK_ITEM, START_TIME, DURATION)
        self.cal.add_timeslice(tc)
        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))

# class Day_entry_test(unittest.TestCase):
#     def test_init(self):
#         day_date = datetime.date(2021, 10, 21)
#         day_entry = Day_entry(day_date)
#         self.assertEquals(day_entry, day_date)
