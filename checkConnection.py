from pprint import pprint
from googleSetup import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'SchedularApp'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def checkConnect():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # print(dir(service))