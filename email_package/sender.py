import os
import pickle
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class GmailSender:
    def __init__(self, credentials_path: str, token_path: str):
        self.creds = None
        self.credentials_path = credentials_path
        self.token_path = token_path
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

    def send_email(self, to: str, subject: str, body: str):
        service = build('gmail', 'v1', credentials=self.creds)
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw}
        try:
            message = (service.users().messages().send(userId="me", body=message_body).execute())
            print(f'Message Id: {message["id"]}')
            return message
        except Exception as error:
            print(f'An error occurred: {error}')
            return None


sender = GmailSender('C:/Users/zino/Downloads/credentials.json', 'token.pickle')
sender.send_email('mujappiah@gmail.com', 'Subject', 'It should work now')
