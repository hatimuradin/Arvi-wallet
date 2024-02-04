from sqlmodel import select

from common.utils import Singleton
from discount.models import ChargeCode, DiscountCode
from discount.database import get_session


class DBHandler(metaclass=Singleton):
    def __init__(self):
        self.db = next(get_session())

    # def update_charge_code(self, phone: str, code: str):
    #     charge_code = self.db.exec(select)

    #     transactions = self.db.exec(query).all()
    #     return transactions
