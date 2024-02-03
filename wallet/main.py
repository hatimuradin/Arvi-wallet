from typing import List
from fastapi import FastAPI, HTTPException

from wallet.crud import DBHandler
from wallet.database import init_db
from wallet.serializers import TransactionResponse

app = FastAPI()
db_handler = DBHandler()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/users/transactions", response_model=List[TransactionResponse])
def read_user_transactions(phone: str):
    """
    Api to return user's list of transactions
    """
    transactions = db_handler.get_user_transactions(phone)
    if transactions is None:
        raise HTTPException(status_code=404, detail="User not found")

    return transactions
