from __future__ import print_function
from pprint import pprint
from datetime import datetime, timedelta
import json
import time
import os
import arrow
from googleSetup import Create_Service

cred = json.dumps(os.getenv("CRED"))
CLIENT_SECRET_FILE = json.loads(cred)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def creatSchedules(x):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    today = datetime.now().date()
    for i in x:
        dict_ = i
        dict = dict_
        event = dict["event"]
        startTime = dict["startTime"]
        endTime = dict["endTime"]

        frmt = "YYYY-MM-DD HH:mm"
        startTime = arrow.get(str(today) + " " + startTime, frmt).isoformat()
        endTime = arrow.get(str(today) + " " + endTime, frmt).isoformat()

        event_result = (
            service.events()
            .insert(
                calendarId="primary",
                sendNotifications=True,
                body={
                    "summary": event,
                    "description": "testing app",
                    "start": {"dateTime": startTime, "timeZone": "America/New_York"},
                    "end": {"dateTime": endTime, "timeZone": "America/New_York"},
                },
            )
            .execute()
        )

        print("created event")
        print("id: ", event_result["id"])
        print("summary: ", event_result["summary"])
        print("starts at: ", event_result["start"]["dateTime"])
        print("ends at: ", event_result["end"]["dateTime"])
