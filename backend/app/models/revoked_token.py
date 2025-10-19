from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class RevokedToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jti: str = Field(index=True, unique=True)
    revoked_at: datetime = Field(default_factory=datetime.utcnow)


