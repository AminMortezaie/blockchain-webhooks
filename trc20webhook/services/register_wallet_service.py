import datetime
import requests
from django.conf import settings
from rest_framework import status
from trc20webhook.services.utils import get_wallet, get_network
from trc20webhook.services.network_services import blockchain_networks
from trc20webhook.models import RegisteredWallet, Network, Wallet


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


def _check_for_registered_wallet(reg_wallet_len: int, network_type: str):
    if (network_type == "WEB3" and reg_wallet_len == 2) or (network_type != "WEB3" and reg_wallet_len == 1):
        return True
    return False


def check_for_registered_wallet(wallet: Wallet, network: Network):
    context = None
    network_type = network.type
    reg_wallet_obj = RegisteredWallet.objects.filter(network=network, wallet=wallet)
    reg_wallet_len = len(reg_wallet_obj)
    if not _check_for_registered_wallet(reg_wallet_len, network_type):
        if network_type == 'WEB3' and reg_wallet_len == 1:
            context = reg_wallet_obj.first().context
        return False, context
    return True, context


def create_registered_wallet(response: dict, network_obj: Network, context: str):
    wallet_address = response['address']
    reference_id = response['referenceId']
    receive_callback_on = response['receiveCallbackOn']
    callback_url = response['callbackUrl']
    created_at = convert_timestamp(str(response['createdTimestamp']))

    try:
        registered_wallet = RegisteredWallet.objects.create(
            network=network_obj, wallet=get_wallet(wallet_address, network_obj),
            reference_id=reference_id, receive_callback_on=receive_callback_on,
            context=context, callback_url=callback_url, created_at=created_at
        )
        return registered_wallet
    except Exception as err:
        print(err)


def _register_wallet(network_obj, context, payload, endpoint):
    payload['context'] = context
    response = get_request_response(endpoint, payload)['data']['item']
    create_registered_wallet(response, network_obj, context)


def retry_register_wallet(network_obj, context, payload, endpoint):
    context = 'tokenTX' if context == 'coinTX' else 'coinTX'
    endpoint = endpoint[context]
    payload['context'] = context
    _register_wallet(network_obj, context, payload, endpoint)


def register_wallet(network: str, wallet: str):
    message = 'wallet registered.'
    status_ = status.HTTP_200_OK

    network_obj = get_network(network)

    if not network_obj:
        pass

    wallet_obj = get_wallet(wallet, network_obj)

    if not wallet_obj:
        pass

    if network_obj.type == 'WEB3':
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
    check_validation, context_validation = check_for_registered_wallet(wallet_obj, network_obj)

    try:
        if check_validation:
            for context, endpoint in endpoints.items():
                payload['context'] = context
                _register_wallet(network_obj, context, payload, endpoint)
        elif not check_validation and context_validation:
            retry_register_wallet(network_obj=network_obj, context=context_validation,
                                  payload=payload, endpoint=endpoints)
        else:
            status_ = status.HTTP_400_BAD_REQUEST
            message = 'Wallet registered before'
    except Exception as err:
        message = str(err)
        status_ = status.HTTP_417_EXPECTATION_FAILED

    return message, status_





