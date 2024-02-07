from pydantic import BaseModel


class ApplyTransaction(BaseModel):
    phone: str
    amount: int


class ApplyTransactionResult(BaseModel):
    phone: str
    result: bool
