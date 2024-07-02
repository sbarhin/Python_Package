import uuid

from basicauth import encode

import requests

from pycomms_pay.payment_package.config import SUBSCRIPTION_KEY, USER_ID, API_KEY

# config.py
API_BASE_URL = "https://sandbox.momodeveloper.mtn.com"


class Momo:
    def __init__(self, api_key, subscription_key, user_id):
        self.api_base_url = API_BASE_URL
        self.api_key = api_key
        self.subscription_key = subscription_key
        self.user_id = user_id
        self.session = requests.Session()
        self.token = ""
        self.auth = str(
            encode(self.user_id, self.api_key))

        self.session.headers.update({
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            # "X-Reference-Id": self.user_id,
            "X-Reference-Id": str(uuid.uuid4()),
            "Content-Type": "application/json",
            "X-Target-Environment": "sandbox",
            "Authorization": str(self.auth),
        })
        self.get_token()

    def get_token(self):
        url = f"{self.api_base_url}/collection/token/"
        response = self.session.post(url)
        response.raise_for_status()
        self.token = response.json().get("access_token")

    def transfer_money(self, amount, currency, external_id, payer, payee_note, payer_message):
        url = f"{self.api_base_url}/collection/v1_0/requesttopay"
        token = self.token
        uuidgen = str(uuid.uuid4())

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": uuidgen,
        }
        self.session.headers.update(headers)
        payload = {
            "amount": amount,
            "currency": currency,
            "externalId": external_id,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": payer
            },
            "payerMessage": payer_message,
            "payeeNote": payee_note
        }
        response = self.session.post(url, json=payload)
        context = {"response": response.status_code, "ref": uuidgen}
        return context

    def momobalance(self):
        url = f"{self.api_base_url}/collection/v1_0/account/balance"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Authorization': "Bearer " + self.token,
            'X-Target-Environment': "sandbox"
        }

        response = self.session.get(url, headers=headers, data=payload)
        json_respon = response.json()

        return json_respon

    def verifymomo(self, txn):
        url = f"{self.api_base_url}/collection/v1_0/requesttopay/" + str(txn) + ""
        payload = {}
        headers = {
            'Authorization': "Bearer " + self.token,
        }
        self.session.headers.update(headers)
        response = self.session.get(url, data=payload)
        json_respon = response.json()

        return json_respon


if __name__ == "__main__":
    momo = Momo(API_KEY, SUBSCRIPTION_KEY, USER_ID)
    pay = momo.transfer_money("1000", "EUR", "123456", "233555417205", "Payment for services", "Thank you")
    if pay['response'] in [200, 202]:
        verify = momo.verifymomo(pay['ref'])
        print(verify)
        balance = momo.momobalance()
        print(balance)
    else:
        print('Something went wrong')
