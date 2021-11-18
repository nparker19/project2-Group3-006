import datetime
import json
import os
from dotenv import load_dotenv, find_dotenv
from googleSetup import Create_Service

load_dotenv(find_dotenv())
cred = json.dumps(os.getenv("CRED"))
CLIENT_SECRET_FILE = json.loads(cred)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def listSchedules():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # Call the Calendar API
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

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
        print(listSchedules())


listSchedules()
