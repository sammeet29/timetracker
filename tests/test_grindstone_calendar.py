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
        self.assertTrue(tc.get_date() in entries)
        self.assertEqual(entries[tc.get_date()][tc.work_item], 15)

    def test_same_entry_twice(self):

        tc = Time_slice(WORK_ITEM, START_TIME, DURATION)
        self.cal.add_timeslice(tc)
        self.cal.add_timeslice(tc)

        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))
        self.assertTrue(tc.get_date() in entries)
        self.assertEqual(entries[tc.get_date()][tc.work_item], 30)

    def test_multiple_entries_same_day(self):
        tc = Time_slice(WORK_ITEM, START_TIME, DURATION)
        self.cal.add_timeslice(tc)

        work_item_2 = 'Work Item 2'
        tc2 = Time_slice(work_item_2, START_TIME, DURATION)
        self.cal.add_timeslice(tc2)

        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))

        self.assertTrue(tc.get_date() in entries)

        day_entry = entries[tc.get_date()]
        self.assertTrue(WORK_ITEM in day_entry)
        self.assertTrue(work_item_2 in day_entry)

        self.assertEqual(day_entry[tc.work_item], 15)
        self.assertEqual(day_entry[work_item_2], 15)

    def test_same_work_item_multiple_days(self):
        tc = Time_slice(WORK_ITEM, START_TIME, DURATION)
        self.cal.add_timeslice(tc)

        start_time2 = '8/17/2021 10:39:16 AM'
        tc2 = Time_slice(WORK_ITEM, start_time2, DURATION)
        self.cal.add_timeslice(tc2)

        entries = self.cal.get_entries()
        self.assertEqual(2, len(entries))

        self.assertTrue(tc.get_date() in entries)
        self.assertTrue(tc2.get_date() in entries)

        day_entry = entries[tc.get_date()]
        self.assertTrue(WORK_ITEM in day_entry)
        self.assertEqual(day_entry[WORK_ITEM], 15)

        day_entry2 = entries[tc2.get_date()]
        self.assertTrue(WORK_ITEM in day_entry2)
        self.assertEqual(day_entry2[WORK_ITEM], 15)
