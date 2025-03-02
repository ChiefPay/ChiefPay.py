from pydantic import BaseModel, Field
from typing import List, Optional

from chiefpay.types.invoice import Address


class Wallet(BaseModel):
    id: str
    order_id: str = Field(alias="orderId")
    addresses: Optional[List[Address]] = Field(default=None)
    uuid: Optional[str] = Field(default=None)