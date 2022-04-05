from datetime import datetime
import sys
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch

sys.path.append('../')
from jira_helper import Jira_helper
from jira_config import SEL_JIRA_URL

class Jira_helper_test(unittest.TestCase):
    @mock.patch('getpass.getpass')
    @mock.patch('getpass.getuser')
    def test_create_session(self, mock_getuser, mock_getpass):
        mock_getuser.return_value = 'sammkoli'
        mock_getpass.return_value = 'passwd'
        j_helper = Jira_helper()

        with patch('requests.post') as mock_request_post:
            mock_request_post.return_value.status_code = 401

            status = j_helper.create_session()

            self.assertEqual(401, status)
            mock_request_post.assert_called_once()

        self.assertTrue(mock_getuser.called)
        self.assertTrue(mock_getpass.called)
        self.assertEqual(j_helper.user, 'sammkoli')

    def test_find_issue(self):
        j_helper = Jira_helper()
        with patch('requests.get') as mock_request:
            TEST_ISSUE = 'RP-8054'
            mock_request.return_value.status_code = 200
            r = j_helper.find_issue(TEST_ISSUE)
            self.assertTrue(mock_request.called)

    def test_add_work_log(self):
        j_helper = Jira_helper()
        with patch('requests.post') as mock_request_post:
            TEST_ISSUE = 'RP-8054'
            TEST_DATE = datetime(2021,8, 16, 10, 39, 16)
            r = j_helper.add_work_log(TEST_ISSUE, 900, TEST_DATE)
            self.assertTrue(mock_request_post.called)
