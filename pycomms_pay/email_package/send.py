import base64
from email.mime.text import MIMEText


def _send_message(service, to, body, subject=''):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw}
    try:
        message = service.users().messages().send(userId="me", body=message_body).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None
