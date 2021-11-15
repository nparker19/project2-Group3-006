from __future__ import print_function
from pprint import pprint
from datetime import datetime, timedelta
from httplib2 import Http
from apiclient.discovery import build

from quickSetUP import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']cl
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

d = datetime.now().date()
tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
start = tomorrow.isoformat()
end = (tomorrow + timedelta(hours=1)).isoformat()

event_result = service.events().insert(calendarId='primary',sendNotifications=True,
body={
    "summary": 'Automating calendar', 
    "description": 'testing app',
    "start": {"dateTime": start, "timeZone": 'America/Los_Angeles'}, 
    "end": {"dateTime": end, "timeZone": 'America/Los_Angeles'},
    }
).execute()

print("created event")
print("id: ", event_result['id'])
print("summary: ", event_result['summary'])
print("starts at: ", event_result['start']['dateTime'])
print("ends at: ", event_result['end']['dateTime'])
print(event_result)