"""
Mocked unit tests for Database functionality
"""


import unittest
from unittest.mock import MagicMock, patch

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

from routes import add_user_email
from models import User_DB

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class UpdateDBTests(unittest.TestCase):
    """
    Class holds all tests for database functionality
    """

    def setUp(self):
        self.db_mock = [User_DB(email="chipaj")]

    def mock_add_to_db(self, email_user):
        self.db_mock.append(email_user)

    def mock_db_commit(self):
        pass

    def test_update_db_ids_for_user(self):
        with patch("routes.User_DB.query") as mock_query:
            with patch("routes.db.session.add", self.mock_add_to_db):
                with patch("routes.db.session.commit", self.mock_db_commit):

                    mock_filtered = MagicMock()

                    # First test where we add an email already in the database
                    mock_filtered.first.return_value = User_DB(email="chipaj")
                    mock_query.filter_by.return_value = mock_filtered

                    add_user_email("chipaj")
                    self.assertEqual(len(self.db_mock), 1)
                    self.assertEqual(self.db_mock[0].email, "chipaj")
                    # Second test, where we add an email not in the database already
                    mock_filtered.first.return_value = None

                    add_user_email("nparker19")
                    self.assertEqual(len(self.db_mock), 2)
                    self.assertEqual(self.db_mock[0].email, "chipaj")
                    self.assertEqual(self.db_mock[1].email, "nparker19")


if __name__ == "__main__":
    unittest.main()
