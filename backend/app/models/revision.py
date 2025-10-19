from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Revision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    problem_id: int = Field(foreign_key="problem.id")
    next_review_date: date
    stage: int
    status: str
    last_attempted_at: Optional[datetime] = None
    user_id: str = Field(foreign_key="user.username")



