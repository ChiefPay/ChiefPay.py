from enum import Enum

BASE_URL = "https://api.chiefpay.org"

class Endpoints(Enum):
    rates = '/v1/rates'
    history = '/v1/history'
    invoice = '/v1/invoice'
    wallet = '/v1/wallet'
    socket = '/socket.io'  # WebSocket endpoint