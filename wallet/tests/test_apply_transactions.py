from unittest import TestCase
from datetime import datetime
from sqlmodel import select

from fastapi.testclient import TestClient

from wallet.database import init_db, drop_db
from wallet.models import User, Wallet, Transaction
from wallet.crud import DBHandler
from wallet.main import app


class ApplyTransactionsTestCase(TestCase):
    def setUp(self):
        init_db()
        self.db = DBHandler().db
        self.db.commit()
        self.client = TestClient(app)
        self.phone = "09109345575"
        self.code = "test_code"
        super().setUp()

    def tearDown(self) -> None:
        drop_db()
        return super().tearDown()

    def test_submit_charge_code(self):
        db = DBHandler().db

        users = [
            User(id=1, phone="1111111111"),
        ]
        db.add_all(users)
        db.flush()

        wallets = [
            Wallet(id=1, last_balance_update=datetime.utcnow(), user_id=1, balance=0),
        ]
        db.add_all(wallets)
        db.flush()

        test_transactions = [
            {"phone": "09101112323", "amount": 1_000_000},
            {"phone": "1111111111", "amount": 500_000},
        ]
        response = self.client.post("/apply-transactions/", json=test_transactions)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(db.exec(select(Transaction)).all()), 2)
        self.assertEqual(
            db.exec(select(Wallet).where(Wallet.user_id == users[0].id))
            .first()
            .balance,
            test_transactions[1].get("amount"),
        )
