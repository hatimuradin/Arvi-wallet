from datetime import datetime
from pydantic import BaseModel


class TransactionResponse(BaseModel):
    uid: str
    amount: int
    created_at: datetime
