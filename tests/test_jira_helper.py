import sys
import unittest
from unittest import mock

sys.path.append('../')
from jira_helper import Jira_helper
from jira_config import SEL_JIRA_URL

class Jira_helper_test(unittest.TestCase):
    @mock.patch('getpass.getuser')
    @mock.patch('getpass.getpass')
    def setUp(self, mock_getpass, mock_getuser):
        mock_getuser.return_value = 'sammkoli'
        mock_getpass.return_value = 'passwd'

        self.j_helper = Jira_helper()

        self.assertTrue(mock_getpass.called)
        self.assertTrue(mock_getpass.called)

        self.assertEqual(self.j_helper.user, 'sammkoli')
        self.assertEqual(self.j_helper.pswd, 'passwd')

    @mock.patch('requests.get')
    def test_find_issue(self, mock_request_get):
        TEST_ISSUE = 'RP-8054'
        r = self.j_helper.find_issue(TEST_ISSUE)
        mock_request_get.assert_called()

    @mock.patch('requests.post')
    def test_add_work_log(self, mock_request_post):
        TEST_ISSUE = 'RP-8054'
        r = self.j_helper.add_work_log(TEST_ISSUE, 900)
        mock_request_post.assert_called()
