import csv
from grindstone_timeslice import Time_slice
from grindstone_calendar import Calendar
from os.path import exists

class Read_grindstone_csv:
    def __init__(self, file_name):
        if(exists(file_name)):
            with open(file_name, encoding='utf-8-sig') as csv_file:
                first_line = csv_file.readline()
                self.is_valid = self.__has_valid_headers(first_line)
                self.file_name = file_name
        else:
            self.is_valid = False

    def get_calendar(self):
        cal = Calendar()
        with open(self.file_name, encoding='utf-8-sig') as csv_file:
            csvreader = csv.DictReader(csv_file)
            for row in csvreader:
                current_time_slice = Time_slice(row['Work Item'], row['Start'], row['Duration'])
                cal.add_timeslice(current_time_slice)
        return cal

    def __has_valid_headers(self, first_line):
        if(first_line.find("Start") == -1 or
        first_line.find("Duration") == -1 or
        first_line.find("Work Item") == -1):
            return False
        return True

def verify_issue(work_item, issue):
    rtn = False
    print('Is JIRA issue:', issue,'correct for', work_item, '?')
    response = input()
    if((response == 'y') or (response == 'Y')):
        rtn = True
    return rtn

def get_issue_from_user(work_item):
    issue = None
    print('Enter Jira issue for the Work Item:', work_item)
    issue = input()
    return issue

def get_issue(work_item):
    from grindstone_calendar import find_issue
    while(True):
        issue = find_issue(work_item)
        if(issue is None):
            issue = get_issue_from_user(work_item)
        if(verify_issue(work_item, issue)):
            break
    return issue

def main():
    import argparse

    parser = argparse.ArgumentParser(prog = "read_grindstone_csv",
        description = "Reads the Grindstone csv")
    parser.add_argument('csv_file', help = 'The grindstone csv file to read from')
    parser.add_argument('-s', action='store_false', dest='silent', default = True, help= 'Do not print the calender')

    args = vars(parser.parse_args())
    csv_file_name = args['csv_file']
    grindstone_file = Read_grindstone_csv(csv_file_name)
    if(not grindstone_file.is_valid):
        print("Invalid file")
        exit()

    cal = grindstone_file.get_calendar()
    if(args['silent']):
        cal.print_calender()

    work_item = cal.get_next_issue()
    while work_item is not None:
        issue = get_issue(work_item)
        work_log = cal.get_work_logs(work_item)
        print(issue)
        for key in work_log.keys():
            from grindstone_calendar import round_up
            print("  ", key, (round_up(work_log[key])/(60 * 60)), 'hrs')
            # log time here
            # log result in a text file!
        work_item = cal.get_next_issue()

    #print log text file

if __name__ == "__main__":
    main()
