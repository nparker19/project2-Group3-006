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
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def isoformatStringFormat(x):
    d_ = dateutil.parser.parse(x)
    dtt = datetime.strptime(str(d_), "%Y-%m-%d %H:%M:%S")    
    # print(dtt)
    return dtt.strftime("%A, %b %d %Y, %H:%M")


def listSchedules():
    service = Create_Service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"
    print("Getting List of 10 shedules")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    events_= []
    starts_ = []
    ends_ = []
    summarys_ = []
    ids_ = []

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        
        print("\n")
        end = event['end'].get('dateTime')  
        print("\n")
        
        summarys_.append(event["summary"])
        ids_.append(event['id'])
        starts_.append(isoformatStringFormat(start))
        ends_.append(isoformatStringFormat(end))
                
        return {
            "events_" : events_,
            "starts_" : starts_,
            "ends_": ends_,
            "summarys_" : summarys_,
            "ids_": ids_,        
        }

listSchedules()
