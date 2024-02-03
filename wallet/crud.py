from sqlmodel import select

from common.utils import Singleton
from wallet.models import Transaction, User, Wallet
from wallet.database import get_session


class DBHandler(metaclass=Singleton):
    def __init__(self):
        self.db = next(get_session())

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
