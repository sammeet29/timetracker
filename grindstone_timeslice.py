from datetime import datetime

class Time_slice:
    def __decode_date(self, start_date_time):
        format = "%m/%d/%Y %I:%M:%S %p"
        tc_start = datetime.strptime(start_date_time, format)
        return tc_start.date()

    def __init__(self, work_item, start, duration):
        self.work_item = work_item
        self.start = start
        self.day_date = self.__decode_date(start)
        self.duration = duration

    def __str__(self):
        return "Name: %s Start:%s Duration:%s" %(self.work_item, self.start, self.duration)

    def get_date(self):
        return self.day_date
