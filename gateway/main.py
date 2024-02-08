import os
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

WALLET_SERVICE_HOST_URL = os.environ.get(
    "WALLET_SERVICE_HOST_URL", "http://wallet_service:8002"
)
DISCOUNT_SERVICE_HOST_URL = os.environ.get(
    "DISCOUNT_SERVICE_HOST_URL", "http://discount_service:8003"
)


@app.get("/api/v1/wallet{full_path:path}")
async def redirect_to_wallet(full_path: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WALLET_SERVICE_HOST_URL}{full_path}")
            return response.text
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/v1/discount{full_path:path}")
async def redirect_to_discount(full_path: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DISCOUNT_SERVICE_HOST_URL}{full_path}")
            return response.text
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
