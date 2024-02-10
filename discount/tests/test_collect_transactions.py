from unittest import TestCase, skip
from datetime import datetime
from fastapi.testclient import TestClient

from discount.main import app
from discount.cache import CacheHandler
from discount.tasks import collect_charge_codes, collect_transactions
from discount.database import init_db, drop_db
from discount.crud import DBHandler
from discount.models import ChargeCode


class CollectTransactionCodesTestCase(TestCase):
    def setUp(self):
        init_db()
        self.db = DBHandler().db
        self.client = TestClient(app)
        self.cache_handler = CacheHandler()
        self.code = "test_code"
        super().setUp()

    def tearDown(self) -> None:
        drop_db()
        self.cache_handler.delete_all()
        return super().tearDown()

    def test_submit_and_collect_charge_code(self):
        test_codes = [
            ChargeCode(
                id=1, amount=10_000, code=self.code, created_at=datetime.utcnow()
            ),
            ChargeCode(
                id=2, amount=20_000, code=self.code, created_at=datetime.utcnow()
            ),
        ]
        self.db.add_all(test_codes)
        self.db.commit()

        response = self.client.post(
            "/charge-code/submit/", json={"code": self.code, "phone": "09109345222"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/charge-code/submit/", json={"code": self.code, "phone": "09102334423"}
        )
        self.assertEqual(response.status_code, 200)

        collect_charge_codes()
        db_code1 = self.db.get(ChargeCode, 1)
        self.assertTrue(db_code1.is_used)

        db_code2 = self.db.get(ChargeCode, 2)
        self.assertTrue(db_code2.is_used)

        collect_transactions()
        db_code1 = self.db.get(ChargeCode, 1)
        self.assertTrue(db_code1.is_applied)

        db_code2 = self.db.get(ChargeCode, 2)
        self.assertTrue(db_code2.is_applied)
