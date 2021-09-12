import csv
from datetime import datetime

class Time_slice:
    def __decode_date(self, start_date_time):
        format = "%m/%d/%Y %I:%M:%S %p"
        return datetime.strptime(start_date_time, format)

    def __init__(self, work_item, start, duration):
        self.work_item = work_item
        self.start = start
        self.day_date = self.__decode_date(start)
        self.duration = duration

    def __str__(self):
        return "Name: %s Start:%s Duration:%s" %(self.work_item, self.start, self.duration)

class Day_items:
    def __init__(self, day_date):
        self.day_date(day_date)
        self.work_slices = {}

    def add_work_item(self, time_slice):
        if(time_slice.work_item in self.work_slices):
            self.work_slices[time_slice.work_item] += time_slice.duration
        else:
            self.work_slices[time_slice.work_item] = time_slice.duration

def main():
    import argparse

    parser = argparse.ArgumentParser(prog = "read_grindstone_csv",
        description = "Reads the Grindstone csv")
    parser.add_argument('csv_file', help = 'The grindstone csv file to read from')

    args = vars(parser.parse_args())
    csv_file = args['csv_file']
    set_of_days = dict()
    with open(csv_file, encoding = 'utf-8-sig') as work_slices:
        csv_reader = csv.DictReader(work_slices)
        for row in csv_reader:
            current_time_slice = Time_slice(row['Work Item'], row['Start'], row['Duration'])
            # calender.add_time_slice(current_time_slice)
            slice_date = current_time_slice.get_date()
            if(slice_date in set_of_days):
                day_items = set_of_days[slice_date]
                day_items.add(current_time_slice)
            else:
                day_item = Day_items(slice_date)
                day_item.add(current_time_slice)
                set_of_days[slice_date] = day_item

if __name__ == "__main__":
    main()
