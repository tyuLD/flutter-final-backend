import os
import warnings

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DEFAULT_DATABASE_URL = "sqlite:///./app.db"


def normalize_database_url(database_url: str) -> str:
    database_url = database_url.strip()
    if database_url.startswith("postgres://"):
        return "postgresql://" + database_url[len("postgres://"):]
    return database_url


raw_database_url = os.getenv("DATABASE_URL")
DATABASE_URL = normalize_database_url(raw_database_url) if raw_database_url else DEFAULT_DATABASE_URL

engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

try:
    engine = create_engine(DATABASE_URL, **engine_kwargs)
except ArgumentError as exc:
    warnings.warn(
        f"Invalid DATABASE_URL value; falling back to {DEFAULT_DATABASE_URL}. Details: {exc}",
        RuntimeWarning,
    )
    DATABASE_URL = DEFAULT_DATABASE_URL
    engine_kwargs = {"connect_args": {"check_same_thread": False}}
    engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()