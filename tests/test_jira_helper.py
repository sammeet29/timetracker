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
