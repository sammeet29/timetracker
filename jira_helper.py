from jira_config import SEL_JIRA_URL
from jira_config import SEL_JIRA_AUTH
from datetime import datetime

# SEL_JIRA_URL = 'dummy.com'
# from jira import JIRA
import getpass
import json
import requests

'''
JIRA rest v2 reference docs
https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/
'''

class Jira_helper:
    def __init__(self):
        self.session = None
        self.user = None
        self.pswd = None

    def create_session(self):
        password = self.__get_password()
        h = { "content-type:  application/json" }
        d = json.dumps({"username": self.user, "password" : password})
        response = requests.post(SEL_JIRA_AUTH, headers=h, data=d)

        status = None
        if(response is not None):
            status = response.status_code
            if(status == 200):
                self.session = response.session

        return status

    """
    The following link explains how to use it
    https://docs.atlassian.com/software/jira/docs/api/REST/8.13.13/#issue-getIssue

    """
    def find_issue(self, issue_id):
        payload = {'fields' : ['id', 'issueType', 'summary', 'status']}
        issue = requests.get(SEL_JIRA_URL+ "issue/" + issue_id, auth=(self.user, self.pswd), params=payload)
        # print(issue.url)
        return issue


    '''
    https://docs.atlassian.com/software/jira/docs/api/REST/1000.824.0/#api/2/issue-addWorklog
    https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-worklogs/#api-rest-api-2-issue-issueidorkey-worklog-post
    '''
    def add_work_log(self, issue_id, time_in_secs, work_log_date):
        url = SEL_JIRA_URL + "issue/" + issue_id + "/worklog"
        UTC_OFFSET_PACIFIC = "-0800"
        payload = json.dumps({
            "timeSpentSeconds" : time_in_secs,
            "started" : work_log_date.isoformat(timespec = 'milliseconds') + UTC_OFFSET_PACIFIC
        })
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        # print(payload)
        return requests.post(url, auth=(self.user, self.pswd), data=payload, headers=headers)

    def __get_password(self):
        self.user = getpass.getuser()
        self.pswd = getpass.getpass(prompt= ("Password for " + self.user + ": "))
        return self.pswd

def main():
    j = Jira_helper()
    TEST_ISSUE = 'RP-8054'
    # issue = j.find_issue('RP-8054')
    # issue = j.get_open_issues()
    START_TIME = '8/16/2021 10:39:16 AM'
    format = "%m/%d/%Y %I:%M:%S %p"
    tc_start = datetime.strptime(START_TIME, format)
    WORK_LOG_DATE = tc_start.date()
    issue = j.add_work_log(TEST_ISSUE, 900, tc_start)
    if(issue is not None):
        print("Issue Status :", issue.status_code)
        issue_json = issue.json()
        print(issue_json)

if __name__ == '__main__':
    main()
