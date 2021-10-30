import datetime
from grindstone_timeslice import Time_slice

class Calendar:
    def __init__(self):
        self.days = {}

    def add_timeslice(self, timeslice):
        timeslice_date = timeslice.get_date()
        if timeslice_date in self.days:
            work_item = timeslice.work_item
            if work_item in self.days[timeslice_date]:
                self.days[timeslice_date][work_item] += timeslice.duration
        else:
            self.days[timeslice_date] = {timeslice.work_item  : timeslice.duration}

    def get_entries(self):
        return self.days

    def clear_entries(self):
        self.days = {}
