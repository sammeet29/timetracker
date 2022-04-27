import unittest
import sys

sys.path.append('../')

from log_time import are_inputs_valid

class Log_time_test(unittest.TestCase):

    def test_are_input_valid_no_action(self):
        from log_time import INVALID_ACTION_MESSAGE

        valid, msg = are_inputs_valid("last_week.csv", False, False, False)
        self.assertFalse(valid)
        self.assertEqual(msg, INVALID_ACTION_MESSAGE)

    def test_are_input_valid_invalid_csv(self):
        from log_time import FILE_DOES_NOT_EXIST_MESSAGE

        valid, msg = are_inputs_valid("invalid_file.csv", True, False, False)
        self.assertFalse(valid)
        self.assertEqual(msg, FILE_DOES_NOT_EXIST_MESSAGE)


