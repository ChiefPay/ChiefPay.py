from pydantic import BaseModel, Field
from typing import List


class Address(BaseModel):
    chain: str
    token: str
    address: str
    token_rate: str = Field(alias='tokenRate')


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
    status: str
    addresses: List[Address]
    description: str
    amount: str
    fiat_details: List[FiatDetails] = Field(alias="FiatDetails")

    class Config:
        populate_by_name = True
