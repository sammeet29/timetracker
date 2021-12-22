import datetime
from grindstone_timeslice import Time_slice

class Calendar:
    def __init__(self):
        self.all_work_items = {}

    def add_timeslice(self, ts):
        ts_wi = ts.get_work_item()
        if ts_wi in self.all_work_items:
            ts_date = ts.get_date()
            ts_duration = ts.get_duration()
            if ts_date in self.all_work_items[ts_wi]:
                self.all_work_items[ts_wi][ts_date] += ts_duration
            else:
                self.all_work_items[ts_wi][ts_date] = ts_duration
        else:
            self.all_work_items[ts_wi] = {ts.get_date()  : ts.get_duration()}

    def get_entries(self):
        return self.all_work_items

    # Returns all the days of the entries in the calender
    def get_calender_days(self):
        list_of_days = self.days.keys()
        return list_of_days

    def print_calender(self):
        for each_day in self.days.keys():
            all_timeslices_for_day = self.days[each_day]
            for each_item in all_timeslices_for_day.keys():
                print("Date " + str(each_day) + \
                    " Work Item: " + each_item + \
                    " Time: " + str(all_timeslices_for_day[each_item]) + " secs")

    def clear_entries(self):
        self.all_work_items = {}
