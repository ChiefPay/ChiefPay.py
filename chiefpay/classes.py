from chiefpay import Client, SocketClient, AsyncClient, AsyncSocketClient
from chiefpay.constants import BASE_URL


class ChiefPay:
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.rest = Client(api_key, base_url)
        self.socket = SocketClient(api_key, base_url)


class AsyncChiefPay:
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.rest = AsyncClient(api_key, base_url)
        self.socket = AsyncSocketClient(api_key, base_url)
