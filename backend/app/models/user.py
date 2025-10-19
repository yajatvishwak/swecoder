from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    password: str
    name: Optional[str] = None



