from twilio.rest import Client


class Sms:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send_message(self, sender, receiver, body):
        try:
            message = self.client.messages.create(
                body=body,
                from_=sender,
                to=receiver
            )
            return {"sid": message.sid, "status": message.status}
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
    acc_sid = 'AC2f939471561b672de056fe39a6708b09'
    auth_token = '4a836d1bfca2a9a39ed510aa7a6890f6'
    phone_number = '+17752590611'

    client = Sms(acc_sid, auth_token)
    res = client.send_message(phone_number, '+233551535009', 'Assalamu alaikum')
    print(f'response {res}')
