from pydantic import BaseModel


class Rate(BaseModel):
    name: str
    rate: str