from datetime import datetime
from fastapi import FastAPI, Response, HTTPException
from discount.crud import DBHandler
from discount.database import init_db
from discount.cache import CacheHandler
from discount.serializers import PhoneNumber, ChargeCodeCacheKey
from discount.tasks import scheduler

db_handler = DBHandler()
cache_handler = CacheHandler()
app = FastAPI()


@app.on_event("startup")
def on_startup():
    # init_db()
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.post("/charge-code/submit/")
def submit_charge_code(data: dict):
    """
    API to receive user charge codes
    """
    if cache_handler.inquiry_charge_codes(
        phone_pattern=data.get("phone"), code_pattern=data.get("code")
    ):
        return Response(status_code=406)

    phone_number = PhoneNumber(number=data.get("phone"))
    code_key = ChargeCodeCacheKey(phone=phone_number, code=data.get("code"))
    cache_handler.set(code_key, datetime.utcnow().isoformat())

    return "Your code is submitted, You'll be notified for the result later"


@app.get("/charge-codes/succeeded-users/{code}/")
def get_succeeded_users_for_code(code: str):
    """
    API to generate report for succeeded users
    """
    try:
        results = db_handler.get_succeeded_users_for_code(code)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error occured generating the report"
        )
