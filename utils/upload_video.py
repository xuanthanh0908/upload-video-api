import os
import argparse
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from api_call.bs import update_status_and_progress_youtube, create_link_for_history

 # Set the API key and OAuth 2.0 client ID
CLIENT_SECRET_FILE = 'secrets/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service(client_secret_file, scopes, channel_id):
    credentials = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(f'{channel_id}.pickle'):
        with open(f'{channel_id}.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            credentials = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open(f'{channel_id}.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    # Build the YouTube API service
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube
  

def upload_video_handler(youtube, video_path, channel_id ,created_by, id, product_id, channel_id_in_ytb):
    video_links = []
    link_prefix = 'https://youtube.com/watch?v='
    files = os.listdir(video_path)

    title = [file for file in files]
    file_paths = [os.path.join(video_path, file) for file in files]
    try:
        ## update video status to running
        update_status_and_progress_youtube(id, {
            'status': 'running'
        })
        for index, file_path in enumerate(file_paths):
            print('index: %d' % index)
            request_body = {
                'snippet': {
                    'title': title[index],
                    'categoryId': '22',  # You can set the category ID according to YouTube's category list,
                    'channelId': channel_id_in_ytb
                },
                'status': {
                    'privacyStatus': 'unlisted',
                },
            }

            media = MediaFileUpload(file_path)

            response = youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=media
            ).execute()
            
            print(f"Video {index + 1} With ID: {response['id']}")
            link_video = link_prefix + response['id']

            video_links.append(response['id'])
            ### DATA ###
            progress_data = {
                '_id': id,
                'current_progress': index + 1,
                'total_progress': len(file_paths),
                'created_by': created_by,
                
            }
            history_data = {
                'product_id': product_id,
                'channel_id': channel_id,
                'created_by': created_by,
                'youtube_url': [{ 
                    'file_name': title[index],
                    'url': link_video,
                  }]
                }
            print(history_data)
            ## create youtube link
            create_link_for_history(history_data, file_path)
            ## update progress
            update_status_and_progress_youtube(id, progress_data)

        ## update video status to completed
        update_status_and_progress_youtube(id, {
            'status': 'completed'
        })
    except Exception as e: 
        update_status_and_progress_youtube(id, {
            'status': 'canceled'
        })
        print (e)


# def main():
#     parser = argparse.ArgumentParser(description='Upload a video to YouTube.')
#     parser.add_argument('video_path', help='Path to the video file')
#     parser.add_argument('--title', default='Your Video Title', help='Title of the video')
#     parser.add_argument('--privacy', choices=['public', 'private', 'unlisted'], default='unlisted', help='Privacy status of the video')
#     args = parser.parse_args()
#     # Set the API key and OAuth 2.0 client ID
#     CLIENT_SECRET_FILE = 'secrets/client_secrets.json'
#     SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
#     # Authenticate the user
#     channel_id = 'UCTOKVs_AhaPoJ8jrZDci8fA'
#     youtube = get_authenticated_service(CLIENT_SECRET_FILE, SCOPES, channel_id)
#     upload_video(youtube, args.video_path, args.title, args.privacy, channel_id)
# if __name__ == '__main__':
#     main()

# python3 upload_video.py "/Users/thanhxuan/Documents/BS/Tools/upload_video_api_projects/231116_DiMTS_HH_Trailer_916.mp4" --title "Your Video Title" --description "Your video description" --tags tag1 tag2 --privacy private