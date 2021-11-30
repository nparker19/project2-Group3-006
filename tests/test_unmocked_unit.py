import unittest
import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from methods import suggest, convertScheduleToRegTime

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class suggestionHelperFunctionTests(unittest.TestCase):
    def test_suggestions_function1(self):
        self.assertEqual(suggest([], []), [])

    def test_suggestions_function2(self):
        inputScheduleDict = [
            {"endTime": "11:00 AM", "event": "IM meeting", "startTime": "10:00 AM"},
            {"endTime": "05:00 PM", "event": "class", "startTime": "03:45 PM"},
        ]
        inputSuggestDict = [
            {"suggestion": "workout", "duration": "1 hour(s) 45 minute(s)"},
            {"suggestion": "study", "duration": "2 hour(s) 0 minute(s)"},
        ]
        outputDict = [
            {
                "suggestStartTime": "11:30 AM",
                "suggestEndTime": "01:15 PM",
                "suggestEvent": "workout",
                "suggestion": "You have enough time to workout between 11:00 AM and 03:45 PM. Would you like to workout from 11:30 AM to 01:15 PM today? (click OK to add to schedule, and click cancel to view any other suggestions)",
            },
            {
                "suggestStartTime": "11:30 AM",
                "suggestEndTime": "01:30 PM",
                "suggestEvent": "study",
                "suggestion": "You have enough time to study between 11:00 AM and 03:45 PM. Would you like to study from 11:30 AM to 01:30 PM today? (click OK to add to schedule, and click cancel to view any other suggestions)",
            },
            {
                "suggestStartTime": "05:30 PM",
                "suggestEndTime": "07:15 PM",
                "suggestEvent": "workout",
                "suggestion": "You have enough time to workout between 05:00 PM and 11:59 PM. Would you like to workout from 05:30 PM to 07:15 PM today? (click OK to add to schedule, and click cancel to view any other suggestions)",
            },
            {
                "suggestStartTime": "05:30 PM",
                "suggestEndTime": "07:30 PM",
                "suggestEvent": "study",
                "suggestion": "You have enough time to study between 05:00 PM and 11:59 PM. Would you like to study from 05:30 PM to 07:30 PM today? (click OK to add to schedule, and click cancel to view any other suggestions)",
            },
        ]
        self.assertEqual(suggest(inputScheduleDict, inputSuggestDict), outputDict)

    def test_timeConverter(self):
        inputDict = [
            {"endTime": "09:00", "event": "nap", "startTime": "8:15"},
            {"endTime": "11:00 AM", "event": "meeting", "startTime": "10:00 AM"},
            {"endTime": "17:00", "event": "class", "startTime": "15:45"},
            {"event": "workout", "startTime": "05:30 PM", "endTime": "06:30 PM"},
        ]
        outputDict = [
            {"event": "nap", "startTime": "08:15 AM", "endTime": "09:00 AM"},
            {"event": "meeting", "startTime": "10:00 AM", "endTime": "11:00 AM"},
            {"event": "class", "startTime": "03:45 PM", "endTime": "05:00 PM"},
            {"event": "workout", "startTime": "05:30 PM", "endTime": "06:30 PM"},
        ]

        self.assertEqual(convertScheduleToRegTime(inputDict), outputDict)


if __name__ == "__main__":
    unittest.main()
