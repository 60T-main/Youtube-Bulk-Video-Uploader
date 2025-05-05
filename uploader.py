import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import time

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def check_creds():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # request login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # save credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

def uploader(creds, video_folder):
    youtube = build("youtube", "v3", credentials=creds)

    videos = os.listdir(path=video_folder)
    video_files = [f for f in videos if f.endswith(".mp4")]

    for video_file in video_files:
        try:
            track_name = os.path.splitext(video_file)[0]
            video_path = os.path.join(video_folder, video_file)
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": f"{track_name}",
                        "description": " ",
                        "categoryId": "10"
                    },
                    "status": {
                        "privacyStatus": "unlisted"
                    }
                },
                media_body=media
            )
            response = request.execute()
            print(f"Uploaded: {video_file}, Video ID: {response['id']}")

        except Exception as e:
            print(f"Failed to upload {video_file}: {str(e)}")
            if 'uploadLimitExceeded' in str(e):
                print("Upload limit exceeded, wait 24 hours to continue...")
                break 
            else:
                print("Retrying in 1 minute...")
                time.sleep(60)








