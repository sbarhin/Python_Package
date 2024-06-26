import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.errors import HttpError
from email_package.auth import get_authenticated_service


def search_emails(service, query):
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_email(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def create_forward_message(original_message, to_email):
    message = MIMEMultipart()
    message['to'] = to_email
    message['subject'] = 'Fwd: ' + original_message['payload']['headers'][0]['value']

    original_message_body = original_message['snippet']
    forward_body = MIMEText(original_message_body)
    message.attach(forward_body)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def forward_email(service, message_id, to_email):
    original_message = get_email(service, message_id)
    if not original_message:
        return

    forward_message = create_forward_message(original_message, to_email)
    try:
        sent_message = (service.users().messages().send(userId='me', body=forward_message).execute())
        print(f'Message forwarded with Id: {sent_message["id"]}')
        return sent_message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def main():
    service = get_authenticated_service()

    # Define your search query
    msgId = '190349e4b294f977   '
    email = get_email(service, msgId)

    if not email:
        print('No email found.')
        return

    # Define the email address to forward to
    forward_to = 'shaubint123@gmail.com'

    forward_email(service, msgId, forward_to)


if __name__ == '__main__':
    main()

# 1902f315f3b3f4fe

# 1902f642c160599d, 190349e4b294f977,, 1902ccc40771fd0f
