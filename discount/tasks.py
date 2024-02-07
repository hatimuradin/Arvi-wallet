import logging
import json

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
from discount.cache import CacheHandler
from discount.crud import DBHandler
from discount.serializers import ChargeCodeCacheKey


cache_handler = CacheHandler()
db_handler = DBHandler()

logger = logging.getLogger(__name__)


def collect_charge_codes():
    """
    This task is responsible for collecting cached submitted charge codes to discount db
    """
    cache_codes = cache_handler.inquiry_charge_codes()
    for c in cache_codes:
        json_code = json.loads(c)
        if not json_code.get("is_collected"):
            try:
                db_handler.use_code(
                    code=json_code.get("code"),
                    phone=json_code.get("phone").get("number"),
                )
                obj = ChargeCodeCacheKey(json_code)
                value = cache_handler.get(obj)
                cache_handler.delete_key_raw(c)
                obj.is_collected = True
                cache_handler.set(obj, value)
            except Exception as e:
                logger.error(
                    f"Unable to collect the cached charge code, reason: {str(e)}"
                )


def collect_transactions():
    """
    This task is responsible for collecting used charged codes from database and send to wallet
    """
    to_be_sent_codes = db_handler.get_not_applied_used_charge_codes()
    ##


# scheduler.add_job(collect_charge_codes, "interval", seconds=1)
# scheduler.add_job(collect_charge_codes, "interval", seconds=5)
