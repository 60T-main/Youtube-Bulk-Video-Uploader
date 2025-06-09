import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import time
import sys


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# program can run via terminal with the main function
def main():
    # if terminal arguments are provided
    import gui 
    if len(sys.argv) == 3:
        folder_path = sys.argv[1]
        print(f"Folder path: '{folder_path}'")
        desc_entry = sys.argv[2]
        
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")
        
        creds = check_creds()
        uploader(creds, folder_path, desc_entry)
    else:
        obj = gui.GUI()
        obj.window.mainloop()

#  check credentials (login info) 
def check_creds():
    creds = None
    # if token exists, pull login info from it
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # if client_secrets.json doesnt exist, explain what to do 
    if not os.path.exists("client_secrets.json"):
        raise FileNotFoundError("Missing 'client_secrets.json'! Please download it from Google Cloud Console and place it in the project directory. More info: https://github.com/60T-main/Youtube-Bulk-Video-Uploader/blob/main/README.md#1-create-a-google-cloud-account")

    # request login if token doesnt exist
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # refreshes token if expired
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # save credentials in token
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

#  begin upload process
def uploader(creds, video_folder, description):
    youtube = build("youtube", "v3", credentials=creds)

    if not check_folder(video_folder):
        print("Folder doesn't exist OR no .mp4 files found")

    # searches .mp4 files in selected folder
    videos = os.listdir(path=video_folder)
    video_files = [f for f in videos if f.endswith(".mp4")]
    

    # uploading individual tracks in folder
    for video_file in video_files:
        try:
            track_name = os.path.splitext(video_file)[0]

            video_path = os.path.join(video_folder, video_file)
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

            # track details
            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": f"{track_name}",
                        "description": f"{description}",
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

        # exceptions
        except Exception as e:
            print(f"Failed to upload {video_file}")
            if 'uploadLimitExceeded' in str(e):
                print("Upload limit exceeded, wait 24 hours to continue... (this restriction is from YouTube)")
                break 
            else:
                print("Retrying in 1 minute...")
                time.sleep(60)

def check_folder(path): #checks if folder exists and has .mp4 files
    return os.path.isdir(path) and any(f.endswith(".mp4") for f in os.listdir(path))


if __name__ == '__main__':
    main()




