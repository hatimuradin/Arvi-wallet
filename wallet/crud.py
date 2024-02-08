from typing import List
from datetime import datetime
from sqlmodel import select
import redis
import uuid

from common.utils import Singleton
from common.serializers import ApplyTransaction
from wallet.models import Transaction, User, Wallet
from wallet.database import get_session
from wallet.settings import WALLET_DB_LOCK_NAME, LOCK_BLOCKING_TIME_OUT, LOCK_TIME_OUT


class DBHandler(metaclass=Singleton):
    def __init__(self):
        self.db = next(get_session())
        self.r = redis.StrictRedis(host="redis-server", port=6379, db=0)

    def get_user_transactions(self, phone: str):
        user = self.db.exec(select(User).where(User.phone == phone)).first()
        if user is None:
            return None

        query = (
            select(Transaction)
            .join(Wallet, Transaction.wallet_id == Wallet.id)
            .where(Wallet.user_id == user.id)
        )
        transactions = self.db.exec(query).all()
        return transactions

    def get_user_balance(self, phone: str):
        user = self.db.exec(select(User).where(User.phone == phone)).first()
        if user is None:
            return None
        query = select(Wallet).where(Wallet.user_id == user.id)
        balance = self.db.exec(query).first()
        return balance

    def apply_transactions(self, transactions: List[ApplyTransaction]):
        with self.r.lock(
            WALLET_DB_LOCK_NAME,
            blocking_timeout=LOCK_BLOCKING_TIME_OUT,
            timeout=LOCK_TIME_OUT,
        ):
            try:
                for t in transactions:
                    phone = t.get("phone")
                    amount = t.get("amount")
                    user = self.db.exec(select(User).where(User.phone == phone)).first()
                    if not user:
                        new_user = User(phone=phone)
                        self.db.add(new_user)
                        self.db.flush()
                        new_wallet = Wallet(user_id=new_user.id)
                        self.db.add(new_wallet)
                        self.db.flush()
                    wallet = self.db.exec(
                        select(Wallet).join(User).where(User.phone == phone)
                    ).first()
                    wallet.balance += amount
                    wallet.last_balance_update = datetime.utcnow()

                    transaction = Transaction(
                        uid=str(uuid.uuid4()),
                        amount=amount,
                        created_at=datetime.utcnow(),
                        wallet_id=wallet.id,
                    )
                    self.db.add(transaction)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise e
