import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from email_package.trash import _trash_message
from email_package.fetching import _list_messages, _get_message
from email_package.send import _send_message

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class Gmail:
    def __init__(self, credentials_path: str, token_path: str):
        self.creds = None
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()

    def _authenticate(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_message(self, to: str, subject: str, body: str):
        return _send_message(self.service, to, body, subject)

    def trash_message(self, message_id):
        _trash_message(self.service, 'me', message_id)

    def messages(self, label_ids=None):
        if label_ids is None:
            label_ids = []
        return _list_messages(self.service, label_ids=label_ids)

    def get_message(self, message_id):
        return _get_message(self.service, message_id)


# all the functions should be here. how move them here
gmail = Gmail('C:/Users/zino/Downloads/credentials.json', 'token.pickle')

# SEND MESSAGE
m_id = gmail.send_message('mujappiah@gmail.com', 'Subject', 'Refactored Class')

# GET MESSAGES
messages = gmail.messages(label_ids=['INBOX'])
for i in messages:
    print(i)

# GET MESSAGE
if len(messages) != 0:
    message = gmail.get_message(messages[0]['id'])

# DELETE MESSAGE
if len(messages) != 0:
    gmail.trash_message(messages[0]['id'])
