from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64

# Your credentials JSON file path (downloaded from Google Cloud Console)
CLIENT_SECRET_FILE = 'C:/Users/zino/Downloads/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)

    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service


def list_messages(service, user_id='me', label_ids=None):
    if label_ids is None:
        label_ids = []
    try:
        # Constructing the query to fetch messages from specific labels (categories)
        query = ''
        if label_ids:
            query = 'label:' + ' label:'.join(label_ids)

        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages

    except Exception as e:
        print(f'An error occurred: {e}')
        return None


def get_message(service, message_id, user_id='me'):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id).execute()
        return message
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


# Main function to fetch and print all messages
def main():
    service = get_gmail_service()
    # FETCHING SPAM MESSAGES
    messages = list_messages(service)
    if messages:
        for message in messages:
            full_message = get_message(service, message['id'])
            if full_message:
                payload = full_message['payload']
                headers = payload['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                print(f'message id: {message["id"]}')
                print(f'Subject: {subject}')


if __name__ == '__main__':
    main()


