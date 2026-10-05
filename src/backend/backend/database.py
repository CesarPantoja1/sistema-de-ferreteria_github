import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def _resolver_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    return "sqlite:///./app.db"


DATABASE_URL = _resolver_database_url()

_connect_args: dict[str, object] = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from backend.catalogo import models  # noqa: F401  (registra las tablas en Base.metadata)

    Base.metadata.create_all(bind=engine)
