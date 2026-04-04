import os.path
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload



SCOPE = ["https://www.googleapis.com/auth/drive"]

default_dir = str(Path(".").absolute()).split("/Lab-muons")[0]+"/Lab-muons/"
universal_dir = lambda path: default_dir + path

LOCAL_FOLDER = universal_dir("Data/timestamp")
token_location = universal_dir("../tokens/")

def authenticate():
    creds = None
    if os.path.exists(token_location+"token.json"):
        creds = Credentials.from_authorized_user_file(token_location+"token.json" , SCOPE)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("token")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(token_location+"client_secret.json" , SCOPE)
            creds = flow.run_local_server( port = 0)
            print("secret file")
        
        with open(token_location+"token.json" , "w") as token:
            token.write( creds.to_json()) # type: ignore
    
    return creds


def sync_local_folder_to_drive():
    creds = authenticate()

    drive_service = build("drive", "v3", credentials=creds)

    about = drive_service.about().get(fields="user").execute()

    about = drive_service.about().get(fields="storageQuota").execute()

    results = drive_service.files().list(
    q="name contains 'Lab Muoni' and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields="files(id, name, owners)"
).execute()

    id_folder = results.get("files", [])[0]["id"]

    query = (
    f"'{id_folder}' in parents and "
    "name contains 'Timestamp' and"
    "mimeType = 'application/vnd.google-apps.folder' and "
    "trashed = false"
)

    results = drive_service.files().list(
        q=query,
        fields="files(id, name, modifiedTime, md5Checksum)"
    ).execute()

    id_subfolder = results.get("files" , [])[0]["id"]

    files_in_subfolder = drive_service.files().list(
    q=f"'{id_subfolder}' in parents and trashed=false",
    fields="files(id, name, modifiedTime)"
).execute()

    file_names = [file["name"] for file in files_in_subfolder.get("files", [])]

    file_to_upload = os.listdir(LOCAL_FOLDER)

    for file in file_to_upload:
        if not file in file_names:
            file_size = os.path.getsize(os.path.join(LOCAL_FOLDER, file))
            print("uploading file:\t", file, f"\t({file_size} bytes)")
            file_path = os.path.join(LOCAL_FOLDER, file)
            file_metadata = {"name": file, "parents": [id_subfolder]}
            media = MediaFileUpload(file_path, resumable=True)
            response = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            if response and "id" in response:
                print(f"Successfully uploaded {file} with ID: {response['id']}")
            else:
                print(f"Failed to upload {file}")

    drive_service.close()

if __name__ == "__main__":
    sync_local_folder_to_drive()