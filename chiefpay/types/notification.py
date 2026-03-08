from pydantic import BaseModel

from chiefpay.types.models import Invoice, Transaction


class NotificationTransaction(BaseModel):
    type: str = "transaction"
    transaction: Transaction


class NotificationInvoice(BaseModel):
    type: str = "invoice"
    invoice: Invoice
