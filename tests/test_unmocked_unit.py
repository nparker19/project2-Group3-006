"""
Unmocked units tests for suggestion generator helper functions
"""

import unittest
import sys
import os

# getting the name of the directory
# where the this file is present.
CURRENT = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
PARENT = os.path.dirname(CURRENT)

# adding the parent directory to
# the sys.path.
sys.path.append(PARENT)

from methods import suggest_generator, convert_schedule_to_reg_time

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class SuggestionHelperFunctionTests(unittest.TestCase):
    """
    Class contains test functions for the suggest_generator
    function and the convert_schedule_to_reg_time function
    """

    def test_suggestions_function1(self):
        self.assertEqual(suggest_generator([], []), [])

    def test_suggestions_function2(self):
        input_schedule_dict = [
            {"endTime": "11:00 AM", "event": "IM meeting", "startTime": "10:00 AM"},
            {"endTime": "05:00 PM", "event": "class", "startTime": "03:45 PM"},
        ]
        input_suggest_dict = [
            {"suggestion": "workout", "duration": "1 hour(s) 45 minute(s)"},
            {"suggestion": "study", "duration": "2 hour(s) 0 minute(s)"},
        ]
        output_dict = [
            {
                "suggestStartTime": "11:30 AM",
                "suggestEndTime": "01:15 PM",
                "suggestEvent": "workout",
                "suggestion": "You have enough time to workout between 11:00 AM and 03:45 PM. Would you like to workout from 11:30 AM to 01:15 PM today? (click OK to add, and click cancel to see more suggestions)",
            },
            {
                "suggestStartTime": "11:30 AM",
                "suggestEndTime": "01:30 PM",
                "suggestEvent": "study",
                "suggestion": "You have enough time to study between 11:00 AM and 03:45 PM. Would you like to study from 11:30 AM to 01:30 PM today? (click OK to add, and click cancel to see more suggestions)",
            },
            {
                "suggestStartTime": "05:30 PM",
                "suggestEndTime": "07:15 PM",
                "suggestEvent": "workout",
                "suggestion": "You have enough time to workout between 05:00 PM and 11:59 PM. Would you like to workout from 05:30 PM to 07:15 PM today? (click OK to add, and click cancel to see more suggestions)",
            },
            {
                "suggestStartTime": "05:30 PM",
                "suggestEndTime": "07:30 PM",
                "suggestEvent": "study",
                "suggestion": "You have enough time to study between 05:00 PM and 11:59 PM. Would you like to study from 05:30 PM to 07:30 PM today? (click OK to add, and click cancel to see more suggestions)",
            },
        ]
        self.assertEqual(
            suggest_generator(input_schedule_dict, input_suggest_dict), output_dict
        )

    def test_time_converter(self):
        input_dict = [
            {"endTime": "09:00", "event": "nap", "startTime": "8:15"},
            {"endTime": "11:00 AM", "event": "meeting", "startTime": "10:00 AM"},
            {"endTime": "17:00", "event": "class", "startTime": "15:45"},
            {"event": "workout", "startTime": "05:30 PM", "endTime": "06:30 PM"},
        ]
        output_dict = [
            {"event": "nap", "startTime": "08:15 AM", "endTime": "09:00 AM"},
            {"event": "meeting", "startTime": "10:00 AM", "endTime": "11:00 AM"},
            {"event": "class", "startTime": "03:45 PM", "endTime": "05:00 PM"},
            {"event": "workout", "startTime": "05:30 PM", "endTime": "06:30 PM"},
        ]

        self.assertEqual(convert_schedule_to_reg_time(input_dict), output_dict)


if __name__ == "__main__":
    unittest.main()
