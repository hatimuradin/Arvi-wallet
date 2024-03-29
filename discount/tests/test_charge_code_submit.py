from datetime import datetime
from fastapi.testclient import TestClient

from discount.main import router
from discount.cache import CacheHandler
from discount.serializers import ChargeCodeCacheKey, PhoneNumber


def test_submit_charge_code():
    client = TestClient(router)
    cache_handler = CacheHandler()
    cache_handler.delete_all()
    phone = "09109345575"
    code = "test_code"

    response = client.post("/charge-code/submit/", json={"code": code, "phone": phone})
    assert response.status_code == 200

    phone_number = PhoneNumber(number=phone)
    code_key = ChargeCodeCacheKey(phone=phone_number, code=code)
    assert cache_handler.get(code_key) != None
