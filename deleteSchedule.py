import datetime
import datetime
import dateutil
from dateutil.parser import *
import json
import os
from dotenv import load_dotenv, find_dotenv
from googleSetup import Create_Service

load_dotenv(find_dotenv())
credentials = json.dumps(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
GOOGLE_APPLICATION_CREDENTIALS = json.loads(credentials)
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def deleteSchedules():
    # Delete the event
    service = Create_Service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )

    
    try:
        service.events().delete(
            calendarId='primary',
            eventId='4kfcd1a9bqegemdn9rdtfgcqg4',
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")
    
    print("Schedule deleted")
    os.lseek
deleteSchedules()