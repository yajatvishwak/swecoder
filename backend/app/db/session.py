from typing import Dict, Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


def _build_connect_args(database_uri: str) -> Dict:
    # SQLite needs this flag for multi-threaded apps like FastAPI with uvicorn
    if database_uri.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(
    settings.sqlmodel_database_uri,
    echo=settings.debug,
    connect_args=_build_connect_args(settings.sqlmodel_database_uri),
    pool_pre_ping=True,
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session



