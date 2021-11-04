import datetime
from grindstone_timeslice import Time_slice

class Calendar:
    def __init__(self):
        self.days = {}

    def add_timeslice(self, ts):
        ts_date = ts.get_date()
        if ts_date in self.days:
            wi = ts.work_item
            if wi in self.days[ts_date]:
                self.days[ts_date][wi] += ts.get_duration()
            else:
                self.days[ts_date][wi] = ts.get_duration()
        else:
            self.days[ts_date] = {ts.work_item  : ts.get_duration()}

    def get_entries(self):
        return self.days

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
        self.days = {}
