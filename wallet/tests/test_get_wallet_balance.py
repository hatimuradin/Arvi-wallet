from datetime import datetime
from fastapi.testclient import TestClient

from wallet.main import app
from wallet.database import init_db, drop_db
from wallet.models import User, Wallet, Transaction
from wallet.crud import DBHandler

client = TestClient(app)


def test_read_user_transactions():
    client = TestClient(app)
    init_db()
    db = DBHandler().db

    users = [
        User(id=1, phone="1111111111"),
    ]
    db.add_all(users)
    db.flush()

    wallets = [
        Wallet(id=1, last_balance_update=datetime.now(), user_id=1, balance=20000),
    ]
    db.add_all(wallets)
    db.flush()

    transactions = [
        Transaction(uid="testuid1", amount=100, wallet_id=wallets[0].id),
        Transaction(uid="testuid2", amount=150, wallet_id=wallets[0].id),
        Transaction(uid="testuid3", amount=250, wallet_id=wallets[0].id),
        Transaction(uid="testuid4", amount=200, wallet_id=wallets[1].id),
    ]
    db.add_all(transactions)
    db.flush()

    response = client.get(f"/users/transactions?phone={users[0].phone}")
    assert response.status_code == 200
    assert len(response.json()) == 3

    drop_db()
