from trc20webhook.services.utils import get_wallet, get_network, get_coin
from rest_framework import status
from trc20webhook.models import TransactionHistory, Wallet, Network, Coin
from trc20webhook.services.network_services import blockchain_networks


def create_transaction(
        tx_hash: str,
        amount: int,
        coin: Coin,
        wallet: Wallet,
        network: Network,
        tx_type: str) -> TransactionHistory:

    tx_type = 'deposit' if tx_type == 'incoming' else 'withdrawal'
    transaction = TransactionHistory.objects.create(transaction_hash=tx_hash, amount=amount,
                                                    coin=coin, network=network, wallet=wallet,
                                                    transaction_type=tx_type)
    return transaction


def set_network_name(network: str) -> str:
    network = blockchain_networks[network]['network_name']
    return network


def filter_payload(request: dict):
    wallet_address = request.data.get('data').get('item').get('address')
    tx_hash = request.data.get('data').get('item').get('transactionId')
    network = set_network_name(request.data.get('data').get('item').get('blockchain'))
    tx_type = request.data.get('data').get('item').get('direction')
    amount = request.data.get('data').get('item').get('amount')
    
    try:
        contract_address = request.data.get('data').get('item').get('token').get('contractAddress')
        amount = request.data.get('data').get('item').get('token').get('amount')
        return wallet_address, tx_hash, network, tx_type, amount, contract_address
    except Exception as e:
        contract_address = ''
        return wallet_address, tx_hash, network, tx_type, amount, contract_address


def generate_transaction(request: dict):
    status_ = status.HTTP_400_BAD_REQUEST
    wallet_address, tx_hash, network, tx_type, amount, contract_address = filter_payload(request)
    try:
        network_obj = get_network(network)
        if not network_obj:
            transaction = 'Network not found!'
            return status_, transaction

        wallet_obj = get_wallet(wallet_address, network_obj)
        if not wallet_obj:
            transaction = 'Wallet not found!'
            return status_, transaction

        coin_obj = get_coin(network_obj, contract_address)
        if not coin_obj:
            transaction = 'Coin not found!'
            return status_, transaction

        create_transaction(
            tx_hash=tx_hash, amount=amount,
            coin=coin_obj, wallet=wallet_obj,
            network=network_obj, tx_type=tx_type
        )

        status_ = status.HTTP_200_OK
        transaction = "transaction successfully gathered."

    except Exception as e:
        transaction = str(e)

    return status_, transaction

