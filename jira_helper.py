import re
from jira_config import SEL_JIRA_URL
from jira_config import SEL_JIRA_AUTH
from datetime import datetime

import getpass
import json
import requests

SESSION_FAILURE = "Session needs to created!"
"""
JIRA rest v2 reference docs
https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/
"""
class JiraHelper:
    """ Class to help with interracting with jira """
    def __init__(self):
        self.session = None
        self.user = None

    def create_session(self):
        """
        Creates a session between the application and server for all future
        requests
        """
        password = self.__get_password()
        session_object = requests.session()
        request_header = { "content-type":  "application/json" }
        request_data = json.dumps({"username": self.user, "password" : password})
        response = session_object.post(SEL_JIRA_AUTH, \
            headers = request_header, data = request_data)

        status_code = 404
        if response is not None:
            status_code = response.status_code
            # print("status Code: ", status_code)
            # print("response.json(): ", response.json)

        # Save the session object only when the login was successful
        if status_code == 200:
            self.session = session_object

        return status_code

    def find_issue(self, issue_id):
        """
        The following link explains how to use it
        https://docs.atlassian.com/software/jira/docs/api/REST/8.13.13/#issue-getIssue
        """
        if self.session is None:
            print(SESSION_FAILURE)
            # throw error here instead
            return None
        payload = {'fields' : ['id', 'issueType', 'summary', 'status']}
        issue = self.session.get(SEL_JIRA_URL+ "issue/" + issue_id, params = payload)

        return issue

    def add_work_log(self, issue_id, time_in_secs, work_log_date):
        """
        https://docs.atlassian.com/software/jira/docs/api/REST/1000.824.0/#api/2/issue-addWorklog
        https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-worklogs/#api-rest-api-2-issue-issueidorkey-worklog-post
        """
        if self.session is None:
            print(SESSION_FAILURE)
            return None

        UTC_OFFSET_PACIFIC = "-0800"
        payload = json.dumps({
            "timeSpentSeconds" : time_in_secs,
            "started" : work_log_date.isoformat(timespec = 'milliseconds') + UTC_OFFSET_PACIFIC
        })
        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        # print(payload)
        url = SEL_JIRA_URL + "issue/" + issue_id + "/worklog"
        return self.session.post(url, data=payload, headers=request_headers)

    def __get_password(self):
        self.user = getpass.getuser()
        pswd = getpass.getpass(prompt= ("Password for " + self.user + ": "))
        return pswd

def main():
    j = JiraHelper()
    TEST_ISSUE = 'RP-8054'
    # issue = j.find_issue('RP-8054')
    # issue = j.get_open_issues()
    START_TIME = '8/16/2021 10:39:16 AM'
    time_stamp_format = "%m/%d/%Y %I:%M:%S %p"
    tc_start = datetime.strptime(START_TIME, time_stamp_format)
    WORK_LOG_DATE = tc_start.date()

    # Functionally test add_work_log
    # issue = j.add_work_log(TEST_ISSUE, 900, tc_start)
    # if(issue is not None):
    #     print("Issue Status :", issue.status_code)
    #     issue_json = issue.json()
    #     print(issue_json)

    session_status = j.create_session()
    if(session_status == 200):
        # issue = j.add_work_log('ROS-1472')
        issue = j.add_work_log(TEST_ISSUE, 900, tc_start)
        if(issue is not None):
            print("Status Code: ", issue.status_code)
            print("Response.json(): ", issue.json())
    else:
        print("Failed to authenticate user")

if __name__ == '__main__':
    main()
