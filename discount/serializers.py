from typing import Annotated, Optional
import datetime
from pydantic import BaseModel


class PhoneNumber(BaseModel):
    number: Annotated[str, r"^((\+989)|(09))\d{9}$"]


class ChargeCodeCacheKey(BaseModel):
    code: str
    phone: PhoneNumber
    is_collected: Optional[bool] = False  # Means collected by task to be mapped on db
