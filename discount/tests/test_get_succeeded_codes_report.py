from unittest import TestCase
from datetime import datetime
from fastapi.testclient import TestClient

from discount.main import app
from discount.database import init_db, drop_db
from discount.crud import DBHandler
from discount.models import ChargeCode


class ReportsTestCase(TestCase):
    def setUp(self):
        init_db()
        self.db = DBHandler().db
        self.db.commit()
        self.client = TestClient(app)
        self.code = "test_code"
        self.phone = "123872632"
        super().setUp()

    def tearDown(self) -> None:
        drop_db()
        return super().tearDown()

    def test_get_reports_for_succeeded_users(self):
        test_codes = [
            ChargeCode(
                id=1,
                code=self.code,
                created_at=datetime.utcnow(),
                is_used=True,
                user_phone="09123445131",
            ),
            ChargeCode(
                id=2,
                code=self.code,
                created_at=datetime.utcnow(),
                is_applied=True,
                user_phone="09123445132",
            ),
            ChargeCode(
                id=3,
                code=self.code,
                created_at=datetime.utcnow(),
                is_used=True,
                is_applied=True,
                user_phone="09123445133",
            ),
            ChargeCode(
                id=4,
                code=self.code,
                created_at=datetime.utcnow(),
                is_used=True,
                is_applied=True,
                user_phone="09123445134",
            ),
        ]
        self.db.add_all(test_codes)
        self.db.flush()

        response = self.client.get(
            f"/charge-codes/succeeded-users/{self.code}/",
        )
        self.assertEqual(response.status_code, 200)
        user_phones = response.json()
        self.assertIn(test_codes[2].user_phone, user_phones)
        self.assertIn(test_codes[3].user_phone, user_phones)
