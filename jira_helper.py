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

    # make this work so as to know what we need to do to get the data
    def find_issue(self, issue_id):
        issue = requests.get(SEL_JIRA_URL+ "issue/" + issue_id, auth=(self.user, self.pswd))
        print(issue.url)
        return issue

    def __authenticate__(self):
        self.user = getpass.getuser()
        self.pswd = getpass.getpass(prompt= ("Password for " + self.user + ": "))

def main():
    j = Jira_helper()
    issue = j.find_issue('RP-1')
    print("Issue Response :",issue)
    # issue_json = issue.json()
    # print(issue_json)

if __name__ == '__main__':
    main()
