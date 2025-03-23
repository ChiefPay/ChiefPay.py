from pydantic import BaseModel, Field
from typing import List, Optional

from chiefpay.types.enums import InvoiceStatus
from chiefpay.types.transaction import LastTransaction


class Address(BaseModel):
    chain: str
    token: str
    method_name: str = Field(alias='methodName')
    address: str
    token_rate: Optional[str] = Field(alias='tokenRate', default=None)


class FiatDetails(BaseModel):
    name: str
    amount: str
    payed_amount: str = Field(alias="payedAmount")
    fee_rate: str = Field(alias="feeRate")
    bank: str
    requisites: str
    card_owner: str = Field(alias="cardOwner")


class Invoice(BaseModel):
    id: str
    order_id: str = Field(alias="orderId")
    payed_amount: str = Field(alias="payedAmount")
    fee_included: bool = Field(alias="feeIncluded")
    accuracy: str
    discount: str
    fee_rate: str = Field(alias="feeRate")
    created_at: str = Field(alias="createdAt")
    expired_at: str = Field(alias="expiredAt")
    status: InvoiceStatus
    addresses: List[Address]
    description: Optional[str] = Field(default=None)
    amount: Optional[str] = Field(default="0")
    fiat_details: Optional[List[FiatDetails]] = Field(alias="FiatDetails", default=None)
    last_transaction: Optional[LastTransaction] = Field(alias="lastTransaction", default=None)
    url: str
    url_success: Optional[str] = Field(alias="urlSuccess", default=None)
    url_return: Optional[str] = Field(alias="urlReturn", default=None)

    class Config:
        populate_by_name = True
