import os 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CLIENT_FILE = 'env/acct1_fjlozadal.json' 
SCOPES = ['https://mail.google.com/']

#access token that allows us to access the api
creds = None

#check if a token file is generated
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
        creds = flow.run_local_server(port=1001)
    with open('token.json','w') as token:
        token.write(creds.to_json())
        
service_gmail = build('gmail','v1',credentials=creds)

dir(service_gmail)        
