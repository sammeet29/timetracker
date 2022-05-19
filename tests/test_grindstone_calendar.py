import unittest

import sys
sys.path.append('../')
from grindstone_calendar import round_up
from grindstone_timeslice import TimeSlice
from grindstone_calendar import Calendar

WORK_ITEM = '1181-ROS QSPI FT'
START_TIME = '8/16/2021 10:39:16 AM'
DURATION = '0:15:32'
TC = TimeSlice(WORK_ITEM, START_TIME, DURATION)


class CalendarTest(unittest.TestCase):
    """ Tests the Grindstone Calendar """

    def setUp(self):
        self.cal = Calendar()
        entries = self.cal.get_entries()
        self.assertEqual(0, len(entries))

    def tearDown(self):
        self.cal.clear_entries()

    def test_single_entry(self):
        """ Tests adding a single entry to calendar"""

        self.cal.add_timeslice(TC)
        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))
        self.assertTrue(TC.work_item in entries)
        self.assertEqual(entries[TC.work_item][TC.get_date()], 932)

    def test_same_entry_twice(self):
        """ Tests adding same entry twice"""

        self.cal.add_timeslice(TC)
        self.cal.add_timeslice(TC)

        entries = self.cal.get_entries()
        self.assertEqual(1, len(entries))

        self.assertTrue(TC.work_item in entries)
        self.assertEqual(entries[TC.work_item][TC.get_date()], 1864)

    def test_multiple_entries_same_day(self):
        """ Tests adding multiple entries on the same day """

        self.cal.add_timeslice(TC)

        work_item_2 = 'Work Item 2'
        tc2 = TimeSlice(work_item_2, START_TIME, DURATION)
        self.cal.add_timeslice(tc2)

        entries = self.cal.get_entries()
        self.assertEqual(2, len(entries))
        self.assertTrue(TC.work_item in entries)
        self.assertTrue(tc2.work_item in entries)

        work_item_1_entries = entries[TC.work_item]
        self.assertEqual(work_item_1_entries,
                         self.cal.get_work_logs(WORK_ITEM))
        self.assertEqual(work_item_1_entries[TC.get_date()], 932)

        work_item_2_entries = entries[tc2.work_item]
        self.assertEqual(work_item_2_entries[tc2.get_date()], 932)

    def test_same_work_item_multiple_days(self):
        """ Tests adding same work item on multiple days """

        self.cal.add_timeslice(TC)

        start_time2 = '8/17/2021 10:39:16 AM'
        tc2 = TimeSlice(WORK_ITEM, start_time2, DURATION)
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

    def test_iterrating_single_entry(self):
        """ Tests the iteration mechanism with a single calendar entry """
        self.cal.add_timeslice(TC)

        work_item = self.cal.get_next_issue()
        work_log = self.cal.get_work_logs(work_item)
        self.assertEqual(1, len(work_log))

        work_item = self.cal.get_next_issue()
        self.assertTrue(work_item is None)

    def test_iterrating_2_entries(self):
        """ Tests the iterating mechanism with more than 1 calendar entry """
        self.cal.add_timeslice(TC)

        work_item_2 = '1205-ROS Review FT code'
        tc2 = TimeSlice(work_item_2, START_TIME, DURATION)
        self.cal.add_timeslice(tc2)

        work_item = self.cal.get_next_issue()
        work_log = self.cal.get_work_logs(work_item)
        self.assertEqual(1, len(work_log))

        work_item = self.cal.get_next_issue()
        work_log = self.cal.get_work_logs(work_item)
        self.assertEqual(1, len(work_log))

        work_item = self.cal.get_next_issue()
        self.assertTrue(work_item is None)

    def test_iterrating_1_work_item_multiple_days(self):
        """
        Tests the iterating mechanism with calendar entries in multiple days
        """

        self.cal.add_timeslice(TC)

        # change start to make it appear as a different log, entries in
        # the same date are merged together
        start = '8/17/2021 10:39:16 AM'
        tc2 = TimeSlice(WORK_ITEM, start, DURATION)
        self.cal.add_timeslice(tc2)

        work_item = self.cal.get_next_issue()
        work_log = self.cal.get_work_logs(work_item)
        self.assertEqual(2, len(work_log))


class RoundOff(unittest.TestCase):
    """ Tests the roundup function """

    def test_already_rounded_time(self):
        """ Tests with a already rounded up time """
        one_hour_in_secs = 60 * 60
        self.assertEqual(one_hour_in_secs, round_up(one_hour_in_secs))

    def test_round_up(self):
        """ Tests if the round up functionality is as expected """
        _37_minutes_in_secs = 37 * 60
        expected_result = 45 * 60  # should be rounded off to 45 minutes
        self.assertEqual(expected_result, round_up(_37_minutes_in_secs))
