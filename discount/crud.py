from typing import List
from datetime import datetime
from sqlmodel import select, and_
import redis

from common.utils import Singleton
from discount.models import ChargeCode, DiscountCode
from discount.database import get_session
from discount.settings import (
    DISCOUNT_DB_LOCK_NAME,
    LOCK_BLOCKING_TIME_OUT,
    LOCK_TIME_OUT,
)


class DBHandler(metaclass=Singleton):
    def __init__(self):
        self.db = next(get_session())
        self.r = redis.StrictRedis(host="redis-server", port="6379", db=0)

    def use_code(self, code: str, phone: str):
        with self.r.lock(
            DISCOUNT_DB_LOCK_NAME,
            blocking_timeout=LOCK_BLOCKING_TIME_OUT,
            timeout=LOCK_TIME_OUT,
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

    def get_not_applied_used_charge_codes(self):
        charge_codes = self.db.exec(
            select(ChargeCode).where(
                and_(ChargeCode.is_used, ChargeCode.is_applied == False)
            )
        ).all()
        return charge_codes

    def get_succeeded_users_for_code(self, code: str) -> List[str]:
        with self.r.lock(
            DISCOUNT_DB_LOCK_NAME,
            blocking_timeout=LOCK_BLOCKING_TIME_OUT,
            timeout=LOCK_TIME_OUT,
        ):
            query = select(ChargeCode).where(
                and_(
                    ChargeCode.is_used,
                    ChargeCode.is_applied,
                    ChargeCode.code == code,
                )
            )
            succeeded_codes = self.db.exec(query).all()
        succeeded_users = [c.user_phone for c in succeeded_codes]
        return succeeded_users
