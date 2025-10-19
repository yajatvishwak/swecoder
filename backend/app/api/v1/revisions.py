from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.problem import Problem
from app.models.revision import Revision
from app.models.user import User
from app.schemas.revision import GetRevisionQuestionsResponse, RevisionQuestion
from app.services.auth import get_current_user


router = APIRouter(prefix="", tags=["revisions"])


@router.get("/get-revision-questions", response_model=GetRevisionQuestionsResponse)
def get_revision_questions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    stmt = select(Revision, Problem).where(
        (Revision.user_id == current_user.username)
        & (Revision.status == "pending")
        & (Revision.next_review_date <= today)
        & (Problem.id == Revision.problem_id)
    )

    rows = session.exec(stmt).all()
    items: List[RevisionQuestion] = []
    for revision, problem in rows:
        late_by = (today - revision.next_review_date).days
        if late_by < 0:
            late_by = 0
        items.append(
            RevisionQuestion(
                problem_id=problem.id,  # type: ignore[arg-type]
                leetcode_slug=problem.leetcode_slug,
                problem_title=problem.problem_title,
                stage=revision.stage,
                next_review_date=revision.next_review_date,
                status=revision.status,
                last_attempted_at=revision.last_attempted_at,
                late_by=late_by,
            )
        )

    return GetRevisionQuestionsResponse(items=items)


