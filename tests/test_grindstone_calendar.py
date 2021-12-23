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

from grindstone_calendar import find_issue
class Find_issue(unittest.TestCase):
    def test_issue_then_project(self):
        actual_issue = find_issue(WORK_ITEM)
        expected_result = "ROS-1181"
        self.assertMultiLineEqual(expected_result, actual_issue)

    def test_proj_then_issue(self):
        work_item = "ROS-1181 QSPI FT"
        actual_issue = find_issue(work_item)
        expected_result = "ROS-1181"
        self.assertMultiLineEqual(expected_result, actual_issue)

    def test_wi_without_issue_name(self):
        work_item = "Admin"
        actual_issue = find_issue(work_item)
        expected_result = ""
        self.assertMultiLineEqual(expected_result, actual_issue)

from grindstone_calendar import round_up
class Round_off(unittest.TestCase):
    def test_already_rounded_time(self):
        one_hour_in_secs = 60 * 60
        self.assertEqual(one_hour_in_secs, round_up(one_hour_in_secs))

    def test_round_up(self):
        _37_minutes_in_secs = 37 * 60
        expected_result = 45 * 60 # should be rounded off to 45 minutes
        self.assertEqual(expected_result, round_up(_37_minutes_in_secs))
