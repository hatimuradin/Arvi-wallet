FROM python:3.11.5-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r discount/requirements.txt

CMD alembic -c discount/alembic.ini upgrade head && uvicorn discount.main:app --reload --host 0.0.0.0 --port 8000
