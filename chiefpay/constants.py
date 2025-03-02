from enum import Enum

BASE_URL = "https://api.chiefpay.org"

class Endpoints(Enum):
    invoices_history = '/v1/history/invoices'
    transactions_history = '/v1/history/transactions'
    rates = '/v1/rates'
    invoice = '/v1/invoice'
    wallet = '/v1/wallet'
    socket = '/socket.io'