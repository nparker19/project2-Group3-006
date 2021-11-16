from __future__ import print_function
from pprint import pprint
from datetime import datetime, timedelta
# from httplib2 import Http
# from apiclient.discovery import build
import time
import arrow
from googleSetup import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# scheduleDict=[{"event":"class", "startTime":"09:00 AM","endTime":"10:04 AM"}, 
#              {"event":"class1", "startTime":"09:00 AM","endTime":"10:04 AM"},
#              {"event":"class1", "startTime":"09:00 AM","endTime":"10:04 AM"}]

def creatSchedules(x):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    today = datetime.now().date()      
    for i in x:
        dict_ = i
        dict = dict_
        event = dict['event']
        startTime = dict['startTime']
        endTime=dict['endTime']

        frmt = 'YYYY-MM-DD HH:mm A'
        startTime = arrow.get(str(today)+' '+ startTime, frmt).isoformat()
        endTime = arrow.get(str(today)+' '+ endTime, frmt).isoformat()

        event_res= service.events().insert(calendarId='primary',sendNotifications=True,
        body={
            "summary": 'event', 
            "description": 'testing app',
            "start": {"dateTime": startTime, "timeZone": 'GMT-5'}, 
            "end": {"dateTime": endTime, "timeZone": 'GMT-5'},
            }
        ).execute()

        print("created event")
        print("id: ", event_res['id'])
        print("summary: ", event_res['summary'])
        print("starts at: ", event_res['start']['dateTime'])
        print("ends at: ", event_res['end']['dateTime'])
        print(event_res)
# creatSchedules(scheduleDict)