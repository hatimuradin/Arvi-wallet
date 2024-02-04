from datetime import datetime
from unittest import TestCase

from discount.serializers import ChargeCodeCacheKey, PhoneNumber
from discount.cache import CacheHandler


class CacheTest(TestCase):
    def setUp(self):
        self.cache_handler = CacheHandler()
        self.phone = "09109234242"
        self.code = "test_code"
        super().setUp()

    def test_set_charge_code_on_cache(self):
        phone = PhoneNumber(number=self.phone)
        dt = datetime.utcnow().isoformat()
        code = ChargeCodeCacheKey(phone=phone, code="test_code")
        self.cache_handler.set(code, dt)
        cache_value = self.cache_handler.get(code)
        self.assertEqual(cache_value, dt)
