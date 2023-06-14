import datetime
import requests
from django.conf import settings
from rest_framework import status
from trc20webhook.services.utils import get_wallet, get_network
from trc20webhook.services.network_services import blockchain_networks
from trc20webhook.models import RegisteredWallets, Network


callback_provider_url = 'https://rest.cryptoapis.io'
CRYPTOAPI_API = settings.CRYPTOAPI_API
HEADERS = {
    'Content-Type': 'application/json',
    'X-API-Key': CRYPTOAPI_API
}


def get_crypto_api_network(network: str) -> str:
    keys_lst = list(blockchain_networks.keys())
    values_lst = list(blockchain_networks.values())

    position = values_lst.index({'network_name': network})
    network = keys_lst[position]
    return network


def register_wallet_endpoint(network: str, type: str) -> str:
    network = get_crypto_api_network(network)
    callback_provider_coin = f"/blockchain-events/{network}/mainnet/subscriptions/address" \
                             "-coins-transactions-confirmed"
    callback_provider_token = f"/blockchain-events/{network}/mainnet/subscriptions/" \
                              "address-tokens-transactions-confirmed"

    endpoint = f"{callback_provider_url}{callback_provider_token}" if type == 'token' \
        else f"{callback_provider_url}{callback_provider_coin}"

    return endpoint


def get_request_response(endpoint: str, payload: dict) -> dict:
    response = requests.post(endpoint, json=payload, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('API request failed with status code', response.status_code)


def convert_timestamp(timestamp: str) -> datetime:
    return datetime.date.fromtimestamp(int(timestamp))


def check_for_registered_wallet(wallet: str, network: Network):
    reg_wallet = RegisteredWallets.objects.filter(network=network, wallet=get_wallet(wallet))
    if len(reg_wallet) == 2:
        return True


def create_registered_wallet(response: dict, network_obj: Network, context: str):
    wallet_address = response['address']
    reference_id = response['referenceId']
    receive_callback_on = response['receiveCallbackOn']
    callback_url = response['callbackUrl']
    created_at = convert_timestamp(str(response['createdTimestamp']))

    try:
        registered_wallet = RegisteredWallets.objects.create(
            network=network_obj, wallet=get_wallet(wallet_address, network_obj),
            reference_id=reference_id, receive_callback_on=receive_callback_on,
            context=context, callback_url=callback_url, created_at=created_at
        )
        return registered_wallet
    except Exception as err:
        print(err)


def register_wallet(network: str, wallet: str):
    message = None
    status_ = status.HTTP_200_OK

    network_obj = get_network(network)
    if network_obj and network_obj.type == 'WEB3':
        coin_endpoint = register_wallet_endpoint(network, type='coin')
        token_endpoint = register_wallet_endpoint(network, type='token')
        endpoints = {
            'coinTX': coin_endpoint,
            'tokenTX': token_endpoint
        }
    else:
        coin_endpoint = register_wallet_endpoint(network, type='coin')
        endpoints = {
            'coinTX': coin_endpoint,
        }

    payload = {
        "context": 'myContext',
        "data": {
            "item": {
                "address": wallet,
                "allowDuplicates": True,
                "callbackUrl": callback_provider_url,
                "receiveCallbackOn": 20
            }
        }
    }
    try:
        for context, endpoint in endpoints.items():
            payload['context'] = context
            response = get_request_response(endpoint, payload)['data']['item']
            create_registered_wallet(response, network_obj, context)
    except Exception as err:
        message = str(err)
        status_ = status.HTTP_417_EXPECTATION_FAILED

    message = 'wallet registered.'
    status_ = status.HTTP_200_OK

    return message, status_





