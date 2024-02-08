FROM python:3.11.5-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r wallet/requirements.txt

CMD alembic -c wallet/alembic.ini upgrade head && uvicorn wallet.main:app --reload --host 0.0.0.0 --port 8000
