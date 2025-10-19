from datetime import datetime
from typing import List, Literal, Optional
from sqlmodel import SQLModel


class StoreSubmissionRequest(SQLModel):
    leetcode_slug: str
    problem_title: Optional[str] = None
    code: str
    is_revision: bool = False
    difficulty: Optional[Literal["easy", "medium", "hard"]] = "medium"

class StoreSubmissionResponse(SQLModel):
    problem_id: int
    submission_id: int
    created_problem: bool


class SolvedQuestion(SQLModel):
    problem_id: int
    leetcode_slug: str
    problem_title: str
    first_solved_date: datetime
    attempts: int


class GetSolvedQuestionsResponse(SQLModel):
    items: List[SolvedQuestion]


