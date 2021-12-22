import unittest
import sys
import datetime

sys.path.append('../')
from grindstone_calendar import Calendar
from grindstone_timeslice import Time_slice

WORK_ITEM = '1181-ROS QSPI FT'
START_TIME = '8/16/2021 10:39:16 AM'
DURATION =  '0:15:32'
TC = Time_slice(WORK_ITEM, START_TIME, DURATION)

class Calendar_test(unittest.TestCase):
    def setUp(self):
        self.cal = Calendar()
        entries = self.cal.get_entries()
        self.assertEqual(0,len(entries))

    def tearDown(self):
        self.cal.clear_entries()

    def test_single_entry(self):
        self.cal.add_timeslice(TC)
        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))
        self.assertTrue(TC.work_item in entries)
        self.assertEqual(entries[TC.work_item][TC.get_date()], 932)

    def test_same_entry_twice(self):
        self.cal.add_timeslice(TC)
        self.cal.add_timeslice(TC)

        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))

        self.assertTrue(TC.work_item in entries)
        self.assertEqual(entries[TC.work_item][TC.get_date()], 1864)

    def test_multiple_entries_same_day(self):
        self.cal.add_timeslice(TC)

        work_item_2 = 'Work Item 2'
        tc2 = Time_slice(work_item_2, START_TIME, DURATION)
        self.cal.add_timeslice(tc2)

        entries = self.cal.get_entries()
        self.assertEqual(2, len(entries))
        self.assertTrue(TC.work_item in entries)
        self.assertTrue(tc2.work_item in entries)

        work_item_1_entries = entries[TC.work_item]
        self.assertEqual(work_item_1_entries[TC.get_date()], 932)

        work_item_2_entries = entries[tc2.work_item]
        self.assertEqual(work_item_2_entries[tc2.get_date()], 932)

    def test_same_work_item_multiple_days(self):
        self.cal.add_timeslice(TC)

        start_time2 = '8/17/2021 10:39:16 AM'
        tc2 = Time_slice(WORK_ITEM, start_time2, DURATION)
        self.cal.add_timeslice(tc2)

        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))

        self.assertTrue(WORK_ITEM in entries)

        work_item_entries = entries[WORK_ITEM]
        self.assertEqual(2, len(work_item_entries))

        self.assertTrue(TC.get_date() in work_item_entries)
        self.assertEqual(work_item_entries[TC.get_date()], 932)

        self.assertTrue(tc2.get_date() in work_item_entries)
        self.assertEqual(work_item_entries[tc2.get_date()], 932)
