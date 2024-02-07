from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class ChargeCode(SQLModel, table=True):
    __tablename__ = "chargecode"

    id: int = Field(primary_key=True, index=True)
    code: str
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()})
    is_used: bool = Field(default=False)  # Means user submitted this code
    used_at: Optional[datetime]
    is_applied: bool = Field(
        default=False
    )  # Means the code is applied on user's wallet
    applied_at: Optional[datetime]
    user_phone: Optional[str]


class DiscountCode(SQLModel, table=True):
    __tablename__ = "discountcode"

    id: int = Field(primary_key=True, index=True)
    code: str
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()})
    is_used: bool = Field(default=False)
    used_at: Optional[datetime]
    is_applied: bool = Field(
        default=False
    )  # Means the code is applied on user's wallet
    applied_at: Optional[datetime]
