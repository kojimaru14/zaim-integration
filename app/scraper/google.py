from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from django.conf import settings
import os

def upload_to_google(file_path, mimetype, new_name, parent_ids):
  SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive']

  json_path = os.path.join(settings.BASE_DIR, "service-account.json")
  sa_creds = service_account.Credentials.from_service_account_file(json_path)
  scoped_creds = sa_creds.with_scopes(SCOPES)
  drive_service = build('drive', 'v3', credentials=scoped_creds)

  upload(drive_service, file_path, mimetype, new_name, parent_ids)

  return True

# Doc on mimetypes: https://developers.google.com/drive/api/v3/mime-types
def upload(drive_service, file_path, mimetype, name, parent_id):
  file_metadata = {'name': name, 'parents': parent_id}
  media = MediaFileUpload(file_path, mimetype=mimetype)
  file = drive_service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
  print ('File ID: %s' % file.get('id'))

  return True