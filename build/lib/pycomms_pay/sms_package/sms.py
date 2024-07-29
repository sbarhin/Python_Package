from twilio.rest import Client

from pycomms_pay.sms_package.config import ACC_SID, PHONE, TOKEN


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

    client = Sms(ACC_SID, TOKEN)
    res = client.send_message(PHONE, '+233551535009', 'Assalamu alaikum')
    print(f'response {res}')
