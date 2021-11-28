import unittest
from unittest.mock import MagicMock, patch

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

from models import User
from routes import addUserEmailDB

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class UpdateDBTests(unittest.TestCase):
    def setUp(self):
        self.db_mock = [User(email="chipaj")]

    def mock_add_to_db(self, email_user):
        self.db_mock.append(email_user)

    def mock_delete_from_db(self, email_user):
        self.db_mock = [
            entry for entry in self.db_mock if entry.email != email_user.email
        ]

    def mock_db_commit(self):
        pass

    def test_update_db_ids_for_user(self):
        with patch("app.User.query") as mock_query:
            with patch("app.db.session.add", self.mock_add_to_db):
                with patch("app.db.session.delete", self.mock_delete_from_db):
                    with patch("app.db.session.commit", self.mock_db_commit):
                        mock_filtered = MagicMock()
                        mock_filtered.all.return_value = self.db_mock

                        mock_filtered.filter.return_value = [User(email="chipaj")]
                        mock_query.filter_by.return_value = mock_filtered

                        # Mocked test 1 (Adding an email which already exists in the DB)
                        addUserEmailDB("chipaj")
                        self.assertEqual(len(self.db_mock), 1)
                        self.assertEqual(self.db_mock[0].email, "chipaj")

                        # Mocked test 1 (Adding an email which does not already exists in the DB)
                        addUserEmailDB("chipaj9912")
                        self.assertEqual(len(self.db_mock), 2)
                        self.assertEqual(self.db_mock[0].email, "chipaj")
                        self.assertEqual(self.db_mock[1].artist_id, "chipaj9912")


if __name__ == "__main__":
    unittest.main()
