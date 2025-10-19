from datetime import date, datetime
from typing import List, Optional

from sqlmodel import SQLModel


class RevisionQuestion(SQLModel):
    problem_id: int
    leetcode_slug: str
    problem_title: str
    stage: int
    next_review_date: date
    status: str
    last_attempted_at: Optional[datetime] = None
    late_by: int


class GetRevisionQuestionsResponse(SQLModel):
    items: List[RevisionQuestion]


