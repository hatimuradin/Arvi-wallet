import os
from typing import Any, List
from pydantic import BaseModel
import redis

from common.utils import Singleton
from discount.serializers import ChargeCodeCacheKey, PhoneNumber

CACHE_PREFIX = os.environ.get("CACHE_PREFIX")


class CacheHandler(metaclass=Singleton):
    def __init__(self):
        self.cache_handler = redis.StrictRedis(
            host="redis_server", port=6379, db=1
        )  # 0 is used for locks
        super().__init__()

    def get(self, object: BaseModel) -> dict:
        key = object.model_dump_json()
        if CACHE_PREFIX:
            key = CACHE_PREFIX + key
        value = self.cache_handler.get(key)
        if value:
            return value.decode("utf-8")

    def get_raw(self, key: str) -> str:
        value = self.cache_handler.get(key)
        if value:
            return value.decode("utf-8")

    def set(self, object: BaseModel, value: Any) -> None:
        key = object.model_dump_json()
        if CACHE_PREFIX:
            key = CACHE_PREFIX + key
        self.cache_handler.set(key, value)

    def set_raw(self, key: str, value: str):
        self.cache_handler.set(key, value)

    def inquiry_charge_codes(
        self,
        code_pattern: str = "*",
        phone_pattern: str = "*",
        is_collected_pattern: str = "*",
    ) -> List[dict]:
        pattern = ChargeCodeCacheKey(
            code=code_pattern,
            phone=PhoneNumber(number=phone_pattern),
        ).model_dump_json()
        if is_collected_pattern == "*":
            pattern.replace("False", "*")
        if is_collected_pattern == "True":
            pattern.replace("False", "True")
        if CACHE_PREFIX:
            pattern = CACHE_PREFIX + pattern
        returned_keys = self.cache_handler.keys(pattern)
        cleaned_keys = [
            (
                key.decode("utf-8").replace(CACHE_PREFIX, "")
                if CACHE_PREFIX
                else key.decode("utf-8")
            )
            for key in returned_keys
        ]
        return cleaned_keys

    def delete_key_raw(self, key):
        k = key
        if CACHE_PREFIX:
            k = CACHE_PREFIX + key
        self.cache_handler.delete(k)

    def delete_all(self, pattern="*"):
        p = pattern
        if CACHE_PREFIX:
            p = CACHE_PREFIX + pattern
        keys = self.cache_handler.keys(p)
        self.cache_handler.delete(*keys)
