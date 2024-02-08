from typing import List
from fastapi import FastAPI, HTTPException, Response

from wallet.crud import DBHandler
from wallet.database import init_db
from wallet.serializers import TransactionResponse, WalletBalance
from common.serializers import ApplyTransaction, ApplyTransactionResult

db_handler = DBHandler()
app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     init_db()


@app.get("/users/{user_phone}/transactions/", response_model=List[TransactionResponse])
def read_user_transactions(user_phone: str):
    """
    API to return user's list of transactions
    """
    transactions = db_handler.get_user_transactions(user_phone)
    if transactions is None:
        raise HTTPException(status_code=404, detail="User not found")

    return transactions


@app.get("/users/{user_phone}/balance/", response_model=WalletBalance)
def read_user_balance(user_phone: str):
    """
    API to return user's balance
    """
    balance = db_handler.get_user_balance(user_phone)
    return balance


@app.post("/apply-transactions/")
def apply_transactions(transactions: List[dict]):
    """
    API to receive transactions
    """
    try:
        db_handler.apply_transactions(transactions)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error occured in applying transactions: {str(e)}"
        )
