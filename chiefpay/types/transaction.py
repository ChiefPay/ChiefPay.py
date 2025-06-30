from pydantic import BaseModel, Field

from chiefpay.types.wallet import Wallet


class Transaction(BaseModel):
    txid: str
    chain: str
    token: str
    value: str
    usd: str
    fee: str
    merchant_amount: str = Field(alias="merchantAmount")
    wallet: Wallet
    created_at: str = Field(alias="createdAt")
    block_created_at: str = Field(alias="blockCreatedAt")


class LastTransaction(BaseModel):
    chain: str
    txid: str
