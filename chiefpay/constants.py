from enum import Enum

BASE_URL = "https://api.chiefpay.org"


class Endpoints(Enum):
    invoices_history = "/v1/history/invoices"
    transactions_history = "/v1/history/transactions"
    rates = "/v1/rates"
    invoice = "/v1/invoice"
    invoice_by_id = "/v1/invoice/{id}"  # For GET/PATCH with path parameter
    invoice_cancel = "/v1/invoice/{id}/cancel"  # For POST cancel
    invoice_prolong = "/v1/invoice/{id}/prolong"  # For POST prolong
    wallet = "/v1/wallet"
    wallet_by_id = "/v1/wallet/{id}"  # For GET with path parameter
    socket = "/socket.io"
