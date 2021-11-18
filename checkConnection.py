from pprint import pprint
import os
from googleSetup import Create_Service
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

credentials = json.dumps(os.getenv("CRED"))
GOOGLE_APPLICATION_CREDENTIALS = json.loads(credentials)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def checkConnect():
    service = Create_Service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    # print(dir(service))


checkConnect()
