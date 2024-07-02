def _list_messages(service, user_id='me', label_ids=None):
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


def _get_message(service, message_id, user_id='me'):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id).execute()
        return message
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


