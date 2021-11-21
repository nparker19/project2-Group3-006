from pprint import pprint
import os
from googleSetup import Create_Service
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

credentials = json.dumps(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
GOOGLE_APPLICATION_CREDENTIALS = json.loads(credentials)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def checkConnect():
<<<<<<< HEAD
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    print(dir(service))
checkConnect()
=======
    service = Create_Service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    # print(dir(service))


checkConnect()
>>>>>>> 174fff7daba68dc4ae55671c6dde4a0331be8f1d
