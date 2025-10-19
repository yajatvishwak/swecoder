from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    createdat: datetime = Field(default_factory=datetime.utcnow, index=True)
    problem_id: int = Field(foreign_key="problem.id")
    user_id: str = Field(foreign_key="user.username")
    is_revision: bool = Field(default=False)



