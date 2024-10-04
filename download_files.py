
# import the required libraries 
import pickle 
import os.path 
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io


# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/drive'] 


def download_file(file_id, file_name, service):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading {file_name}: {int(status.progress() * 100)}% complete.")
    fh.close()


def getFileList(folder_id: str): 
    creds = None

    # Check if file token.pickle exists 
    if os.path.exists('token.pickle'): 
  
        # Read the token from the file and store it in the variable creds 
        with open('token.pickle', 'rb') as token: 
            creds = pickle.load(token) 
  
    # If no valid credentials are available, request the user to log in. 
    if not creds or not creds.valid: 
  
        # If token is expired, it will be refreshed, else, we will request a new one. 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            flow = InstalledAppFlow.from_client_secrets_file( 
                'credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0) 
  
        # Save the access token in token.pickle file for future usage 
        with open('token.pickle', 'wb') as token: 
            pickle.dump(creds, token) 
  
    # Connect to the API service 
    service = build('drive', 'v3', credentials=creds) 
  
    query = f"'{folder_id}' in parents"
    results = service.files().list(
        q=query, fields="nextPageToken, files(id, name)").execute()
    
    items = results.get('files', [])
    results = []
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            if not os.path.exists(f"user_input/{item['name']}"):
                print(f'item name: {item["name"]}')
                print(f'Split: {item["name"].split(" ")}')
                type, name = item['name'].split(" ")
                name = name.replace(".jpg", "").replace("-", " ")
                try:
                    download_file(item['id'], f"user_input/{item['name']}", service)
                except HttpError as e:
                    break
                print(f"File {item['name']} downloaded.")
                results.append({'type': type, 'name': name, 'filename': item['name']})
            else:
                print(f"File {item['name']} already exists.")
    return results
  

