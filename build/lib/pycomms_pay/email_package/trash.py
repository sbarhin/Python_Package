def _trash_message(service, user_id, message_id):
    try:
        service.users().messages().trash(userId=user_id, id=message_id).execute()
        print(f'Message with ID: {message_id} deleted successfully.')
        # else:
        #     print('Failed')
    except Exception as e:
        print(f'An error occurred: {e}')
