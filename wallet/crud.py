from sqlalchemy.orm import Session, aliased
from sqlmodel import select, and_, alias, join

from common.utils import Singleton
from wallet.models import Transaction, User, Wallet
from wallet.database import get_session


class DBHandler(metaclass=Singleton):
    def __init__(self):
        self.db = next(get_session())

    def get_user_transactions(self, phone: str):
        user = self.db.exec(select(User).where(User.phone == phone)).first()
        if user is None:
            return None  # Or you can raise an exception if you prefer

        # transactions = (
        #     self.db.query(Transaction, Wallet, User)
        #     .join(Transaction)
        #     .join(Wallet)
        #     .join(User)
        #     .filter(User.id == Wallet.user_id)
        #     .filter(Transaction.wallet_id == Wallet.id)
        #     .all()
        # )
        query = (
            select(Transaction)
            .join(Wallet, Transaction.wallet_id == Wallet.id)
            .where(Wallet.user_id == user.id)
        )
        transactions = self.db.exec(query).all()

        return transactions
