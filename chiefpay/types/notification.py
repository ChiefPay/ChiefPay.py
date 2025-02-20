from pydantic import BaseModel

from chiefpay.types.invoice import Invoice
from chiefpay.types.transaction import Transaction


class NotificationTransaction(BaseModel):
    type: str = "transaction"
    transaction: Transaction


class NotificationInvoice(BaseModel):
    type: str = "invoice"
    invoice: Invoice
