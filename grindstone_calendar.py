import re

class Calendar:
    """ Calendar class to store all the work logs """

    def __init__(self):
        # stores all the work items and the logging info
        self.all_work_items = {}
        # used for iterating over all the worklogs
        self.work_item_keys = []
        self.entry_index = 0


    def add_timeslice(self, time_slice):
        """
        Add timeslice to the calendar

        :param time_slice: Time slice or work log to add to the calendar
        """
        ts_wi = time_slice.get_work_item()
        if ts_wi in self.all_work_items:
            ts_date = time_slice.get_date()
            ts_duration = time_slice.get_duration()
            if ts_date in self.all_work_items[ts_wi]:
                self.all_work_items[ts_wi][ts_date] += ts_duration
            else:
                self.all_work_items[ts_wi][ts_date] = ts_duration
        else:
            self.all_work_items[ts_wi] = \
                {time_slice.get_date(): time_slice.get_duration()}

    def get_entries(self):
        """ Returns all work logs as a dictionary """
        return self.all_work_items


    def get_work_logs(self, work_item):
        """
        Given the work item, gives all the work logs related to it.

        :param work_item : Work item for which the work logs need to be found

        Returns : All the time slices for a work item. None otherwise
        """
        return self.all_work_items[work_item]


    def get_next_issue(self):
        """
        Returns the next work item.
        This needs to be reset before using it again.

        Returns : Next work item from the list of all work items.
        """
        if not self.work_item_keys:
            self.work_item_keys = list(self.all_work_items.keys())
            work_item = self.work_item_keys[0]
            self.entry_index = 0
        else:
            self.entry_index += 1
            work_item = None
            if self.entry_index < len(self.work_item_keys):
                work_item = self.work_item_keys[self.entry_index]
        return work_item


    def reset_iterator(self):
        """ Resets the iterator by emptying the list of work items """
        self.work_item_keys = []


    def print_calender(self):
        """ Prints out the Calendar entry to system out """
        #TODO: This needs a test
        for key, value in self.all_work_items.items():
            print("Work Item :" + key)
            for each_day_key, each_day_value in value.items():
                print("  Date " + str(each_day_key) +
                      "  Time: " + str(each_day_value) + " secs")


    def clear_entries(self):
        """
        Clear Calendar entries
        """
        self.all_work_items = {}
        self.reset_iterator()


def find_issue(wi_name):
    """
    Looks for a JIRA issue number in a string

    :param wi_name : Work Item name string of the work log

    Returns: JIRA issue if found, else None.
    """
    number_pattern = re.compile('\d+')
    number_match = number_pattern.search(wi_name)

    project_pattern = re.compile('(-[a-z|A-Z]+)|([a-z|A-Z]+-)')
    proj_match = project_pattern.search(wi_name)

    issue = None
    if (number_match is not None) and (proj_match is not None):
        issue_number = number_match.group()
        proj = proj_match.group().strip(" -")  # remove space and '-'
        issue = proj + '-' + issue_number
    return issue


def round_up(time_in_secs):
    """
    Rounds up the time to quarter of an hour.

    :param time_in_secs : Time in secs

    Returns: Time rounded up to quarter of an hour in secs
    """
    secs_in_15_minutes = 15 * 60
    if (time_in_secs % secs_in_15_minutes) == 0:
        time = time_in_secs
    else:
        round_down = int(time_in_secs / secs_in_15_minutes)
        time = (round_down * secs_in_15_minutes) + secs_in_15_minutes

    return time
