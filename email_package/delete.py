import requests

from email_package.auth import get_authenticated_service


def list_messages(service, user_id='me', query=''):
    try:
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


def delete_message(service, user_id, message_id):
    try:
        headers = {
            'Authorization': 'Bearer ' + 'ya29.a0AXooCgvGeDD7nSBMt7qQ9wADYfwPbrBToUluJAFYP-raHiurJRWulnOHVCdHuk2LDd9sBUrLaKzDqyncOMl7WVk4lGIxfeNsL0TjAanzsiQB6rBA0bXCNv5aEjunB6YLAprTvQAs5jIffNFOAl_jOvk7FqJD8rBt_LBlaCgYKAc0SARMSFQHGX2MiTMS5Hjt5Ip7UR2kF5S8oXw0171'}
        response = requests.post(
            f'https://gmail.googleapis.com/gmail/v1/users/{user_id}/messages/{message_id}/trash?key=AIzaSyA7RBhpJDtGb1558PGnM5_Chavsv3a1UKM',
            headers=headers)
        print(f'response {response.text}')
        if response.status_code == 200:
            # service.users().messages().delete(userId=user_id, id=message_id).execute()
            print(f'Message with ID: {message_id} deleted successfully.')
        else:
            print('Failed')
    except Exception as e:
        print(f'An error occurred: {e}')


# Main function to search and delete emails

def main():
    service = get_authenticated_service()
    delete_message(service, 'me', '19049a7a7491d978')


if __name__ == '__main__':
    main()

# 19049a7a7491d978
# 1903d463098d02a0
# 1903d3b2861f075b
