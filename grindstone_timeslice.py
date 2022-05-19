from datetime import datetime


class TimeSlice:
    """
    Class to store a unit of recordable time slice
    """
    def get_work_item(self):
        """
        Gets the work Item of the time slice

        Returns: The work item of the time slice.
        """
        return self.work_item

    def get_date(self):
        """
        Gets the date of the Time slice as a Date() object

        Returns: Date of the time slice
        """
        return self.day_date

    def get_duration(self):
        """
        Gets the duration of timeslice in seconds

        Returns: Duration of the timeslice in seconds
        """
        return self.duration_secs

    def __decode_date(self, start_date_time):
        time_stamp_format = "%m/%d/%Y %I:%M:%S %p"
        tc_start = datetime.strptime(start_date_time, time_stamp_format)
        return tc_start.date()

    # converts the duration into secs
    def __decode_duration(self, duration):
        t_list = duration.split(":")
        time_in_secs = int(t_list[0]) * 360 + \
            int(t_list[1]) * 60 + int(t_list[2])
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
