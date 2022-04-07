from datetime import datetime
import sys
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch
import json

sys.path.append('../')
from jira_helper import Jira_helper
from jira_config import SEL_JIRA_URL

# This class will be used to fake a response object
class Fake_response():
    def __init__(self):
        # store the status_code of the response
        self.status_code = 404
        # store the response in text format
        self.text = ""

    # return a json object from the text
    def json(self):
        return json.loads(self.text)

class Fake_session():
    def __init__(self, response = Fake_response()):
        self.response = response
        self.get_called = False
        self.post_called = False
        self.put_called = False

    def get(self, url, headers = None, data = None):
        self.get_called = True
        return self.response

    def post(self, url, headers = None, data = None):
        self.post_called = True
        return self.response

    def put(self, url, headers = None, data = None):
        self.put_called = True
        return self.response

class Jira_helper_test(unittest.TestCase):
    @mock.patch('getpass.getpass')
    @mock.patch('getpass.getuser')
    def test_create_session_failure(self, mock_getuser, mock_getpass):
        mock_getuser.return_value = 'sammkoli'
        mock_getpass.return_value = 'passwd'
        j_helper = Jira_helper()

        with patch('requests.session') as mock_request_session:
            mock_session = Fake_session()
            mock_request_session.return_value = mock_session

            status = j_helper.create_session()

            self.assertEqual(404, status)
            mock_request_session.assert_called_once()
            self.assertTrue(mock_session.post_called)

        self.assertTrue(mock_getuser.called)
        self.assertTrue(mock_getpass.called)
        self.assertEqual(j_helper.user, 'sammkoli')
        self.assertIsNone(j_helper.session)

    def test_create_session_expected_operation(self):
        jh = Jira_helper()
        valid_response = Fake_response()
        valid_response.status_code = 200
        valid_response.text = json.dumps({
            'session': {
                'name': 'JSESSIONID',
                'value': '699C0594C3BB19DBC6E8810888F81E21'
            },
            'loginInfo': {
                'failedLoginCount': 93,
                'loginCount': 9285,
                'lastFailedLoginTime': '2022-03-25T15:40:22.372-0700',
                'previousLoginTime': '2022-04-05T22:11:25.847-0700'
            }
        })
        with patch("getpass.getuser") as mock_getuser:
            with patch("getpass.getpass") as mock_getpass:
                with patch("requests.session") as mock_session:
                    mock_getuser.return_value = 'sammkoli'
                    mock_getpass.return_value = 'password'
                    s = Fake_session(valid_response)
                    mock_session.return_value = s
                    # mock_requests_post.return_value = valid_response
                    status = jh.create_session()

                    self.assertEqual(status, 200)
                    self.assertIsNotNone(jh.session)

    # def test_find_issue_expected_operation(self):
    #     j_helper = Jira_helper()
    #     with patch('requests.get') as mock_request:
    #         TEST_ISSUE = 'RP-8054'
    #         mock_request.return_value.status_code = 200
    #         r = j_helper.find_issue(TEST_ISSUE)
    #         self.assertTrue(mock_request.called)

    def test_find_issue_invalid_session(self):
        j_helper = Jira_helper()
        r = j_helper.find_issue('RP-8054')
        self.assertIsNone(r)

    def test_add_work_log(self):
        j_helper = Jira_helper()
        with patch('requests.post') as mock_request_post:
            TEST_ISSUE = 'RP-8054'
            TEST_DATE = datetime(2021,8, 16, 10, 39, 16)
            r = j_helper.add_work_log(TEST_ISSUE, 900, TEST_DATE)
            self.assertTrue(mock_request_post.called)
