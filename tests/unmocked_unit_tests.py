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

from methods import suggest

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class getSuggestionsTests(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                INPUT: [],
                EXPECTED_OUTPUT: (""),
            },
            {
                INPUT: {
                    [
                        {"event": "class", "time": "09:00 AM"},
                        {"event": "meeting", "time": "06:30 PM"},
                        {"event": "meeting2", "time": "10:00 PM"},
                    ]
                },
                EXPECTED_OUTPUT: (
                    "You have a good amount of time between class and meeting You could get in a workout and a study session. ",
                    "You have some time between meeting and meeting2. This would be a great time to study or get in quick nap.",
                ),
            },
        ]

    def test_accept_suggestions(self):
        for test in self.success_test_params:
            self.assertEqual(suggest(test[INPUT]), test[EXPECTED_OUTPUT])


"""
class GetCombinedSongArtistsStringTests(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                INPUT: [],
                EXPECTED_OUTPUT: "",
            },
            {
                INPUT: [{"name": "Artist1"}],
                EXPECTED_OUTPUT: "Artist1",
            },
            {
                INPUT: [{"name": "Artist1"}, {"name": "Artist2"}],
                EXPECTED_OUTPUT: "Artist1, Artist2",
            },
        ]

    def test_get_combined_song_artists_string(self):
        for test in self.success_test_params:
            self.assertEqual(
                get_combined_song_artists_string(test[INPUT]), test[EXPECTED_OUTPUT]
            )



VERSION 2: ONE TEST CASE PER FUNCTION
This is the test case organization method I prefer, but I didn't
cover it in class. Note how it frees us up to test multiple helper
functions in a single class.



class SpotifyHelperTests(unittest.TestCase):
    def test_extract_song_data_1(self):
        self.assertEqual(extract_song_data({}), (None, None, None, None))

    def test_extract_song_data_2(self):
        self.assertEqual(
            extract_song_data({"name": "Song Name"}), ("Song Name", None, None, None)
        )

    def test_extract_song_data_3(self):
        # This is a big enough JSON that we should probably split it out for
        # readability
        song_json = {
            "name": "Song Name",
            "artists": [{"name": "Artist"}],
            "album": {"images": [{"url": "image_url"}]},
            "preview_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        self.assertEqual(
            extract_song_data(song_json),
            (
                "Song Name",
                "Artist",
                "image_url",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            ),
        )

    def test_get_combined_song_artists_string_1(self):
        self.assertEqual(get_combined_song_artists_string([]), "")

    def test_get_combined_song_artists_string_3(self):
        self.assertEqual(
            get_combined_song_artists_string([{"name": "Artist1"}]), "Artist1"
        )

    def test_get_combined_song_artists_string_2(self):
        self.assertEqual(
            get_combined_song_artists_string(
                [{"name": "Artist1"}, {"name": "Artist2"}]
            ),
            "Artist1, Artist2",
        )
"""


if __name__ == "__main__":
    unittest.main()
