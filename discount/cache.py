from typing import Any, List
from pydantic import BaseModel
import redis

from common.utils import Singleton


class CacheHandler(metaclass=Singleton):
    def __init__(self):
        self.cache_handler = redis.StrictRedis()
        super().__init__()

    def get(self, object: BaseModel) -> dict:
        value = self.cache_handler.get(object.model_dump_json())
        if value:
            return value.decode("utf-8")

    def set(self, object: BaseModel, value: Any) -> None:
        self.cache_handler.set(object.model_dump_json(), value)

    def inquiry(self, pattern: str) -> List[dict]:
        return self.cache_handler.keys(pattern)
