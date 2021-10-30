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
                self.days[ts_date][wi] += ts.duration_dec
            else:
                self.days[ts_date][wi] = ts.duration_dec
        else:
            self.days[ts_date] = {ts.work_item  : ts.duration_dec}

    def get_entries(self):
        return self.days

    def clear_entries(self):
        self.days = {}
