from typing import Optional

from sqlmodel import Field, SQLModel


class Problem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    leetcode_slug: str = Field(index=True)
    problem_title: str
    attempts: int = 0
    user_id: str = Field(foreign_key="user.username")



