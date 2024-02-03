import os

from sqlmodel import create_engine, SQLModel, Session


DATABASE_URL = os.environ.get("WALLET_DATABASE_URI")

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def init_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
