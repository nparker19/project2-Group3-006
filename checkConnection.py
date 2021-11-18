from pprint import pprint
import os
from googleSetup import Create_Service
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

cred = json.dumps(os.getenv("CRED"))
CLIENT_SECRET_FILE = json.loads(cred)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def checkConnect():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # print(dir(service))


checkConnect()
