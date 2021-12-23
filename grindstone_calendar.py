import datetime
from grindstone_timeslice import Time_slice

class Calendar:
    def __init__(self):
        self.all_work_items = {}
        self.work_item_keys = []

    '''
    Add timeslice to the calendar
    '''
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

    """
    Given the work item, gives all the work logs related to it.

    Returns : None if it does not exist
    """
    def get_work_logs(self, work_item):
        return self.all_work_items[work_item]

    """
    Returns the next work item.
    This needs to be reset before using it again.
    """
    def get_next_issue(self):
        if (len(self.work_item_keys) == 0):
            self.work_item_keys = list(self.all_work_items.keys())
            work_item = self.work_item_keys[0]
            self.entry_index = 0
        else:
            self.entry_index += 1
            work_item = None
            if(self.entry_index < len(self.work_item_keys)):
                work_item = self.work_item_keys[self.entry_index]
        return work_item

    def reset_iterator(self):
        self.work_item_keys = []

    def print_calender(self):
        for each_item in self.all_work_items.keys():
            days = self.all_work_items[each_item]
            print("Work Item :" + each_item)
            for each_day in days.keys():
                print("  Date " + str(each_day) + \
                    " Time: " + str(days[each_day]) + " secs")

    '''
    Clear Calendar entries
    '''
    def clear_entries(self):
        self.all_work_items = {}
        self.reset_iterator()

def find_issue(wi_name):
    import re
    number_pattern = re.compile('\d+')
    number_match = number_pattern.search(wi_name)

    project_pattern = re.compile('(-[a-z|A-Z]+)|([a-z|A-Z]+-)')
    proj_match = project_pattern.search(wi_name)

    if((number_match is None) | (proj_match is None)):
        return ""
    else:
        issue_number = number_match.group()
        proj = proj_match.group().strip(" -") # remove space and '-'
        return proj + '-' + issue_number

def round_up(time_in_secs):
    _15_MINS_IN_SECS = 15 * 60
    if((time_in_secs % _15_MINS_IN_SECS) == 0):
        time = time_in_secs
    else:
        round_down = int(time_in_secs / _15_MINS_IN_SECS)
        time = (round_down * _15_MINS_IN_SECS) + _15_MINS_IN_SECS

    return time
