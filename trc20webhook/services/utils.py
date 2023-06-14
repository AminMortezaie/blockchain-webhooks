from trc20webhook.models import Wallet, Network, Coin


def get_wallet(wallet_address: str, network: Network) -> Wallet | None:
    try:
        wallet_obj = Wallet.objects.filter(address=wallet_address, network=network)
        return wallet_obj
    except Wallet.DoesNotExist:
        pass


def get_network(network: str) -> Network | None:
    try:
        network_obj = Network.objects.get(symbol=network)
    except Network.DoesNotExist:
        try:
            network_obj = Network.objects.get(name=network.capitalize())
        except Network.DoesNotExist:
            network_obj = None
    return network_obj


def get_coin(network: Network, contract_address: str) -> Coin | None:
    try:
        coin_obj = Coin.objects.filter(network=network, contract_address=contract_address)
        return coin_obj
    except Coin.DoesNotExist:
        pass

