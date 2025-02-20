from pydantic import BaseModel, Field

from chiefpay.types.wallet import Wallet


class Transaction(BaseModel):
    txid: str
    chain: str
    token: str
    value: str
    usd: str
    fee: str
    wallet: Wallet
    created_at: str = Field(alias='createdAt')
    block_created_at: str = Field(alias='blockCreatedAt')