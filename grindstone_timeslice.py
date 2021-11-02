from datetime import datetime

class Time_slice:
    def get_date(self):
        return self.day_date

    def get_duration(self):
        return self.duration_secs

    def __decode_date(self, start_date_time):
        format = "%m/%d/%Y %I:%M:%S %p"
        tc_start = datetime.strptime(start_date_time, format)
        return tc_start.date()

    # converts the duration into secs
    def __decode_duration(self, duration):
        t_list = duration.split(":")
        time_in_secs = int(t_list[0]) * 60 + int(t_list[1])
        return time_in_secs

    def __init__(self, work_item, start, duration):
        self.work_item = work_item
        self.start = start
        self.day_date = self.__decode_date(start)
        self.duration = duration
        self.duration_secs = self.__decode_duration(duration)

    def __str__(self):
        return \
            "Name " + self.work_item + \
            " Duration " + self.duration + \
            " or " + str(self.duration_secs) + " secs"
