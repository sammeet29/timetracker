from jira_config import SEL_JIRA_URL

# SEL_JIRA_URL = 'dummy.com'
# from jira import JIRA
import getpass
import json
import requests

class Jira_helper:
    def __init__(self):
        self.__authenticate__()
        # self.jira = JIRA(SEL_JIRA_URL)
        # print("Jira helper")

    """
    The following link explains how to use it
    https://docs.atlassian.com/software/jira/docs/api/REST/8.13.13/#issue-getIssue

    """
    def find_issue(self, issue_id):
        payload = {'fields' : ['id', 'issueType', 'summary', 'status']}
        issue = requests.get(SEL_JIRA_URL+ "issue/" + issue_id, auth=(self.user, self.pswd), params=payload)
        print(issue.url)
        return issue

    def __authenticate__(self):
        self.user = getpass.getuser()
        self.pswd = getpass.getpass(prompt= ("Password for " + self.user + ": "))

def main():
    j = Jira_helper()
    issue = j.find_issue('RP-8054')
    print("Issue Response :", issue)
    if(issue is not None):
        issue_json = issue.json()
        print(issue_json)

if __name__ == '__main__':
    main()
