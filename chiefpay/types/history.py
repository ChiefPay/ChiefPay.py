from pydantic import BaseModel

from chiefpay.types.invoice import Invoice


class History(BaseModel):
    type: str
    invoice: Invoice