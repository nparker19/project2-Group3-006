"""
the script is check the google authentication is working,
the is to collect imput from wepy interface
and pass it to google API service to create calender when
createschedule function is called
"""
from __future__ import print_function
import os
import json
import datetime
from datetime import datetime
import dateutil
from dotenv import load_dotenv, find_dotenv
import arrow
import googleapiclient
# from pprint import pprint
from googlesetup import create_service

load_dotenv(find_dotenv())

credentials = json.dumps(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
GOOGLE_APPLICATION_CREDENTIALS = json.loads(credentials)
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def check_connect():
    """
    the function is used to check that aouth authorization is working
    """
    service = create_service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    print(dir(service))

def create_schedules(xitems):
    """
    the method get input from react input and pass it
    to google calender to make calender
    """
    service = create_service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    today = datetime.now().date()
    for i in xitems:
        dicct_ = i
        dicct = dicct_
        event = dicct["event"]
        start_time = dicct["startTime"]
        end_time = dicct["endTime"]
        frmt = "YYYY-MM-DD HH:mm A"
        start_time = arrow.get(str(today) + " " + start_time, frmt).isoformat()
        end_time = arrow.get(str(today) + " " + end_time, frmt).isoformat()

        # disable pylint googlecalmethods.py:57:12: E1101: 
        # Instance of 'Resource' has no 'events' member (no-member)
        event_result = (
            service.events()
            .insert(
                calendarId="primary",
                sendNotifications=True,
                body={
                    "summary": event,
                    "description": "testing app",
                    "start": {"dateTime": start_time, "timeZone": "America/New_York"},
                    "end": {"dateTime": end_time, "timeZone": "America/New_York"},
                },
            )
            .execute()
        )
    print(event_result)
    
    # disable pylint py:72:0: C0103: Argument name "x" 
    # doesn't conform to snake_case naming style (invalid-name)
def isoformat_string_format(x):
    """
    This method to convert isoformat time from API to string format
    """
    date_ = dateutil.parser.parse(x)
    dtt = datetime.strptime(str(date_), "%Y-%m-%d %H:%M:%S")
    return dtt.strftime("%A, %b %d %Y, %H:%M")

# disable pylint py:94:8: E1101: Instance of 'Resource'
#  has no 'events' member (no-member)
def list_schedules():
    """
    This script call google calendar API and
    and call class object service to put API to use
    link the google calendar for users
    """
    service = create_service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"
    print("Getting List of 10 shedules")
    events_json = (
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

    events = events_json.get("items", [])
    events_ = []
    starts_ = []
    ends_ = []
    summarys_ = []
    ids_ = []
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime")
        summarys_.append(event["summary"])
        ids_.append(event["id"])
        starts_.append(isoformat_string_format(start))
        ends_.append(isoformat_string_format(end))
        return {
            "events_": events_,
            "starts_": starts_,
            "ends_": ends_,
            "summarys_": summarys_,
            "ids_": ids_,
        }
# disable pylint py:136:8: E1101: Instance of 'Resource' 
# has no 'events' member (no-member)
def delete_schedules():
    """
    the function is to delete the event from google calender
    """
    service = create_service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES
    )
    try:
        service.events().delete(
            calendarId='primary',
            eventId='4kfcd1a9bqegemdn9rdtfgcqg4',
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")
    print("service")
