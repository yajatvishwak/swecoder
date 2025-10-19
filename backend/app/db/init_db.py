from sqlmodel import SQLModel

from app.db.session import engine


def init_db() -> None:
    # Register models for metadata
    from app import models  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)


