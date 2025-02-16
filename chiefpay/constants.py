from enum import Enum

API_VERSION = "v1"
BASE_URL = f"https://api.chiefpay.org/{API_VERSION}"


class Endpoints(Enum):
    rates = '/rates',
    history = '/history',
    invoice = '/invoice',
    wallet = '/wallet',
    socket = '/socket.io'