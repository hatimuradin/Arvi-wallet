from datetime import datetime
from fastapi import FastAPI, HTTPException
from discount.crud import DBHandler
from discount.database import init_db
from discount.cache import CacheHandler
from discount.serializers import PhoneNumber, ChargeCodeCacheKey

app = FastAPI()
db_handler = DBHandler()
cache_handler = CacheHandler()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/charge-code/submit/")
def submit_charge_code(data: dict):
    """
    API to receive user charge codes
    """
    phone_number = PhoneNumber(number=data.get("phone"))
    code_key = ChargeCodeCacheKey(phone=phone_number, code=data.get("code"))
    if cache_handler.get(code_key):
        raise HTTPException(status_code=406, details="This code already submitted")
    cache_handler.set(code_key, datetime.utcnow().isoformat())

    return "Your code is submitted, You'll be notified for the result later"
