from read_grindstone_csv import Read_grindstone_csv

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

    parser = argparse.ArgumentParser(prog = "Log time",
        description = "Reads a grindstone csv file and logs time to JIRA")
    parser.add_argument('csv_file', help = 'The grindstone csv file to read from')
    parser.add_argument('-n', action='store_true', dest='dry_run', default= False, help = 'Do a dry run')
    parser.add_argument('-f', action='store_true', dest='post_logs', default= False, help = 'Post all the time logs')
    parser.add_argument('-i', action='store_true', dest='interactive', default = False, help = 'Add the Issue number before logging')

    args = vars(parser.parse_args())
    csv_file_name = args['csv_file']
    grindstone_file = Read_grindstone_csv(csv_file_name)
    if(not grindstone_file.is_valid):
        print("Invalid file")
        exit()

    dry_run = args['dry_run']
    post_logs = args['post_logs']
    interactive = args['interactive']

    if(not(dry_run or post_logs or interactive)):
        print("No action specified")
        exit()

    if(dry_run):
        cal = grindstone_file.get_calendar()
        cal.print_calender()

    # if(interactive):
    #     cal = grindstone_file.get_calendar()
    #     work_item = cal.get_next_issue()
    #     while work_item is not None:
    #         issue = get_issue(work_item)
    #         work_log = cal.get_work_logs(work_item)
    #         print(issue)
    #         for key in work_log.keys():
    #             from grindstone_calendar import round_up
    #             print("  ", key, (round_up(work_log[key])/(60 * 60)), 'hrs')
    #             # log time here
    #             # log result in a text file!
    #         work_item = cal.get_next_issue()

    #print log text file

if __name__ == "__main__":
    main()
