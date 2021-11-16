import datetime
from googleSetup import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'SchedularApp'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def listSchedules():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting List of 5 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
# print(listSchedules())
listSchedules()