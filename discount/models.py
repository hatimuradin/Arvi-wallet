from datetime import datetime
from sqlmodel import SQLModel, Field


class ChargeCode(SQLModel):
    id: int = Field(primary_key=True, index=True)
    code: str
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()})
    is_used: bool = Field(default=False)  # Means user submitted this code
    used_at: datetime = Field(default=None)
    is_applied: bool = Field(
        default=False
    )  # Means the code is applied on user's wallet
    applied_at: datetime = Field(default=None)


class DiscountCode(SQLModel):
    id: int = Field(primary_key=True, index=True)
    code: str
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()})
    is_used: bool = Field(default=False)
    used_at: datetime = Field(default=None)
    is_applied: bool = Field(
        default=False
    )  # Means the code is applied on user's wallet
    applied_at: datetime = Field(default=None)
