from typing import List
from pydantic import BaseModel, ConfigDict, Field

from chiefpay.types.models import Invoice, Transaction


class InvoicesHistory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    invoices: List[Invoice]
    total_count: int = Field(alias='totalCount')


class TransactionsHistory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    transactions: List[Transaction]
    total_count: int = Field(alias='totalCount')