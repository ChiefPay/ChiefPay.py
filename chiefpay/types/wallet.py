from pydantic import BaseModel, Field
from typing import List

from chiefpay.types.invoice import Address


class Wallet(BaseModel):
    id: str
    order_id: str = Field(alias="orderId")
    addresses: List[Address]