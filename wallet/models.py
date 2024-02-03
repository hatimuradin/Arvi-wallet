from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    phone: str = Field(unique=True)

class Wallet(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    balance: int = Field(default=0)
    last_balance_update: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()})
    user_id: int = Field(default=None, foreign_key="user.id", unique=True)

class Transaction(SQLModel, table=True):
    uid: str = Field(unique=True, primary_key=True)
    amount: int = Field(default=0)
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()})
    wallet_id: int = Field(default=None, foreign_key="user.id")
