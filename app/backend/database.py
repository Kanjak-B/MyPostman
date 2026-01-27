from __future__ import annotations

from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.backend.core.config import settings

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

db_url = settings.database_url
if db_url.startswith("sqlite:///./data/"):
    db_path = DATA_DIR / "app.db"
    db_url = f"sqlite:///{db_path.as_posix()}"

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
