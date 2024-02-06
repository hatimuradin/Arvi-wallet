from unittest import TestCase
from datetime import datetime
from fastapi.testclient import TestClient

from discount.main import app
from discount.cache import CacheHandler
from discount.serializers import ChargeCodeCacheKey, PhoneNumber
from discount.tasks import collect_charge_codes
from discount.database import init_db, drop_db
from discount.crud import DBHandler
from discount.models import ChargeCode


class SumbitChargeCodeTestCase(TestCase):
    def setUp(self):
        init_db()
        self.db = DBHandler().db
        self.client = TestClient(app)
        self.cache_handler = CacheHandler()
        self.phone = "09109345575"
        self.code = "test_code"
        super().setUp()

    def tearDown(self) -> None:
        drop_db()
        self.cache_handler.delete_all()
        return super().tearDown()

    def test_submit_and_collect_charge_code(self):
        test_code = ChargeCode(id=1, code="test_code", created_at=datetime.utcnow())
        self.db.add(test_code)
        self.db.commit()

        response = self.client.post(
            "/charge-code/submit/", json={"code": self.code, "phone": self.phone}
        )
        self.assertEqual(response.status_code, 200)

        phone_number = PhoneNumber(number=self.phone)
        code_key = ChargeCodeCacheKey(phone=phone_number, code=self.code)
        self.assertIsNotNone(self.cache_handler.get(code_key))

        collect_charge_codes()
        db_code = self.db.get(ChargeCode, 1)
        self.assertTrue(db_code.is_used)
        self.assertEqual(db_code.user_phone, self.phone)
