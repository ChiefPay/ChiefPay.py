from pydantic import BaseModel, Field


class Wallet(BaseModel):
    id: str
    order_id: str = Field(alias="orderId")