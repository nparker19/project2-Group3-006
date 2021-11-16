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

from methods import suggest, sortDictTimeMilitary

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class getSuggestionsTests(unittest.TestCase):
    def test_suggestions_function1(self):
        self.assertEqual(suggest([]), [])

    def test_suggestions_function2(self):
        inputDict = [
            {"event": "class", "startTime": "09:00", "endTime": "10:45"},
            {"event": "meeting", "startTime": "18:30", "endTime": "19:00"},
            {"event": "meeting2", "startTime": "22:00", "endTime": "23:15"},
        ]
        outputList = [
            "You have over 5 hours of free time between class and meeting. You could get in a workout and a study session!",
            "You have a few hours of free time between meeting and meeting2. This would be a great time to study or get in quick nap.",
        ]
        self.assertEqual(suggest(inputDict), outputList)

    def test_military_sort(self):
        inputDict = [
            {"event": "class", "startTime": "09:00", "endTime": "10:45"},
            {"event": "meeting2", "startTime": "22:00", "endTime": "23:15"},
            {"event": "meeting", "startTime": "18:30", "endTime": "19:00"},
        ]
        outputDict = [
            {"event": "class", "startTime": "09:00", "endTime": "10:45"},
            {"event": "meeting", "startTime": "18:30", "endTime": "19:00"},
            {"event": "meeting2", "startTime": "22:00", "endTime": "23:15"},
        ]

        self.assertEqual(suggest(inputDict), outputDict)


if __name__ == "__main__":
    unittest.main()
