from datetime import datetime
from sqlmodel import select
import redis

from common.utils import Singleton
from discount.models import ChargeCode, DiscountCode
from discount.database import get_session
from discount.settings import DISCOUNT_DB_LOCK_NAME, LOCK_BLOCKING_TIME_OUT


class DBHandler(metaclass=Singleton):
    def __init__(self):
        self.db = next(get_session())
        self.r = redis.StrictRedis(db=0)

    def use_code(self, code: str, phone: str):
        with self.r.lock(
            DISCOUNT_DB_LOCK_NAME, blocking_timeout=LOCK_BLOCKING_TIME_OUT
        ):
            try:
                query = select(ChargeCode).where(
                    (ChargeCode.code == code) & (ChargeCode.is_used == False)
                )
                available_code = self.db.exec(query).first()
                if available_code:
                    available_code.used_at = datetime.utcnow()
                    available_code.is_used = True
                    available_code.user_phone = phone
                    self.db.commit()
            except:
                self.db.rollback()

    # def update_charge_code(self, phone: str, code: str):
    #     charge_code = self.db.exec(select)

    #     transactions = self.db.exec(query).all()
    #     return transactions
