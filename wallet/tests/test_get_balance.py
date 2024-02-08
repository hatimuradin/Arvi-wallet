from datetime import datetime
from fastapi.testclient import TestClient

from wallet.main import router
from wallet.database import init_db, drop_db
from wallet.models import User, Wallet, Transaction
from wallet.crud import DBHandler


def test_read_user_transactions():
    client = TestClient(router)
    init_db()
    db = DBHandler().db

    users = [
        User(id=1, phone="1111111111"),
    ]
    db.add_all(users)
    db.flush()

    wallets = [
        Wallet(id=1, last_balance_update=datetime.utcnow(), user_id=1, balance=20000),
    ]
    db.add_all(wallets)
    db.flush()

    response = client.get(f"/users/{users[0].phone}/balance/")
    assert response.status_code == 200
    assert response.json() == {"balance": wallets[0].balance}

    drop_db()
