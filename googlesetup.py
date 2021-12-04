"""
This script is to call  gooogle calender API for use in app.
"""
import pickle
import os
import datetime
import json
from dotenv import load_dotenv, find_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

load_dotenv(find_dotenv())

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=""):
    """
    this unit is defined for handing calendar API calling
    """
    # decide to keep variable as this despict pylint suggestion:
    # pylint: disable=C0103
    # pylint: disable=W0621: Redefining name 'API_VERSION' from outer scope (line 69) 
    # (redefined-outer-name)
    # pylint: disable=W0621: Redefining name 'SCOPES' from outer scope (line 70) 
    # (redefined-outer-name)
    # pylint: disable=W0621: Redefining name 'service' from outer scope (line 74) 
    # (redefined-outer-name)
    # pylint: disable= R1721: Unnecessary use of a comprehension,
    # use list(scopes[0]) instead. (unnecessary-comprehension)
    
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    working_dir = os.getcwd()
    token_dir = "token_files"
    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle"

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()
       
        # pylin: disable W0703: Catching too general exception Exception (broad-except)
        with open(os.path.join(working_dir, token_dir, pickle_file), "wb") as token:
            pickle.dump(cred, token)
    # refuse to follow pylint suggestion here to
    # maintain the this app work as it is now
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, API_VERSION, "service created successfully")
        return service
    except Exception as error:
        print(error)
        print(f"Failed to create service instance for {API_SERVICE_NAME}")
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None

def convert_to_rfc_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    """
    function convert time to datatime format
    """
    dttime = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + "Z"
    return dttime

if __name__ == "__main__":
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = json.dumps(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    GOOGLE_APPLICATION_CREDENTIALS = json.loads(credentials)

    service = create_service(
        GOOGLE_APPLICATION_CREDENTIALS, API_NAME, API_VERSION, SCOPES, "x"
    )
