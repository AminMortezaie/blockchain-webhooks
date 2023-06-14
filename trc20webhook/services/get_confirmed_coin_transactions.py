import json

import requests


# address = "TD56nP3ma3anFC1eZGb8yqYZgfjKegAVsK"

# callback_provider_url = 'https://rest.cryptoapis.io'

# callback_provider_new_confirmed_coins_transactions = "/blockchain-events/tron/nile/subscriptions/" \
#                                                      "address-coins-transactions-confirmed"

# payload = {
#     "context": "tronConfirmedCoinTx",
#     "data": {
#         "item": {
#             "address": "TD56nP3ma3anFC1eZGb8yqYZgfjKegAVsK",
#             "allowDuplicates": True,
#             "callbackUrl": "https://example.com",
#             "receiveCallbackOn": 1
#         }
#     }
# }

# headers = {
#     'Content-Type': 'application/json',
#     'X-API-Key': 'b509d28104aa4a81a28fdd7822e8f515049eda1a'
# }

# querystring = {"context": "tronConfirmedCoinTx"}


class ConfirmedTransactionsCallback:
    @staticmethod
    def register_confirmed_coin_callback(
            callback_provider_url,
            callback_provider_new_confirmed_coins_transactions,
            payload,
            headers
    ):
        json_pyload = json.dumps(payload)
        response = requests.post(callback_provider_url + callback_provider_new_confirmed_coins_transactions,
                                 json=json_pyload,
                                 headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('API request failed with status code', response.status_code)

    @staticmethod
    def register_confirmed_token_callback(
            callback_provider_url,
            callback_provider_new_confirmed_coins_transactions,
            payload,
            headers
    ):
        json_pyload = json.dumps(payload)
        response = requests.post(callback_provider_url + callback_provider_new_confirmed_coins_transactions,
                                 json=json_pyload,
                                 headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('API request failed with status code', response.status_code)
