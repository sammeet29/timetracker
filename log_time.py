

def main():
    import argparse

    parser = argparse.ArgumentParser(prog = "Log time",
        description = "Reads a grindstone csv file and logs time to JIRA")
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
