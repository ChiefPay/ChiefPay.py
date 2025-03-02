from typing import List
from pydantic import BaseModel, Field

from chiefpay.types.invoice import Invoice
from chiefpay.types.transaction import Transaction


class InvoicesHistory(BaseModel):
    invoices: List[Invoice]
    total_count: int = Field(alias='totalCount')


class TransactionsHistory(BaseModel):
    transactions: List[Transaction]
    total_count: int = Field(alias='totalCount')