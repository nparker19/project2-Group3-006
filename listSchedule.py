import datetime
import json
import os
from dotenv import load_dotenv, find_dotenv
from googleSetup import Create_Service

load_dotenv(find_dotenv())
credentials = json.dumps(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
GOOGLE_APPLICATION_CREDENTIALS = json.loads(credentials)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def listSchedules():
    service = Create_Service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    # Call the Calendar API
<<<<<<< HEAD
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting List of 5 shedules')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
=======
    now = datetime.datetime.utcnow().isoformat() + "Z"
    print("Getting List of 5 shedules")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

>>>>>>> 174fff7daba68dc4ae55671c6dde4a0331be8f1d
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
        print(listSchedules())
<<<<<<< HEAD
        print(events)
listSchedules()
=======


listSchedules()
>>>>>>> 174fff7daba68dc4ae55671c6dde4a0331be8f1d
