from typing import Annotated
import datetime
from pydantic import BaseModel, constr


class PhoneNumber(BaseModel):
    number: Annotated[str, r"^((\+989)|(09))\d{9}$"]


class ChargeCodeCacheKey(BaseModel):
    code: str
    phone: PhoneNumber
