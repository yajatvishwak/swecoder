from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func

from app.db.session import get_session
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.user import User
from app.models.revision import Revision
from app.schemas.submission import StoreSubmissionRequest, StoreSubmissionResponse, GetSolvedQuestionsResponse, SolvedQuestion
from app.services.auth import get_current_user


router = APIRouter(prefix="", tags=["submissions"])

REVISION_STAGES = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

@router.post("/store-submission", response_model=StoreSubmissionResponse, status_code=status.HTTP_201_CREATED)
def store_submission(
    payload: StoreSubmissionRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Ensure user exists (from token)
    user = session.get(User, current_user.username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Auto-generate problem_title from slug if not provided
    problem_title = payload.problem_title or payload.leetcode_slug.replace('-', ' ').title()
    
    # Find or create problem for this user and slug
    statement = select(Problem).where(
        (Problem.user_id == current_user.username) & (Problem.leetcode_slug == payload.leetcode_slug)
    )
    problem = session.exec(statement).first()

    created_problem = False
    if not problem:
        problem = Problem(
            leetcode_slug=payload.leetcode_slug,
            problem_title=problem_title,
            attempts=1,
            user_id=current_user.username,
        )
        session.add(problem)
        session.commit()
        session.refresh(problem)
        created_problem = True
    else:
        # Optionally increment attempts on new submission
        problem.attempts = (problem.attempts or 0) + 1
        session.add(problem)
        session.commit()

    submission = Submission(
        code=payload.code,
        problem_id=problem.id,  # type: ignore[arg-type]
        user_id=current_user.username,
        is_revision=payload.is_revision,
    )
    session.add(submission)
    session.commit()
    session.refresh(submission)

    # Create initial revision entry if none exists for this problem and user
    existing_revision = session.exec(
        select(Revision).where(
            (Revision.problem_id == problem.id) & (Revision.user_id == current_user.username)
        )
    ).first()

    if not existing_revision:
        revision = Revision(
            problem_id=problem.id,  # type: ignore[arg-type]
            next_review_date=date.today() + timedelta(days=REVISION_STAGES[0]),
            stage=0,
            status="pending",
            last_attempted_at=datetime.utcnow(),
            user_id=current_user.username,
        )
        session.add(revision)
        session.commit()
    else:
        if payload.is_revision:
            if payload.difficulty == "easy":
                existing_revision.stage += 1 if existing_revision.stage < len(REVISION_STAGES) - 1 else 0
            elif payload.difficulty == "medium":
                existing_revision.stage -= 1 if existing_revision.stage > 0 else 0
            elif payload.difficulty == "hard":
                existing_revision.stage = 0
            existing_revision.next_review_date = date.today() + timedelta(days=REVISION_STAGES[existing_revision.stage])
            existing_revision.status = "pending"
        existing_revision.last_attempted_at = datetime.utcnow()
        session.add(existing_revision)
        session.commit()

    return StoreSubmissionResponse(
        problem_id=problem.id,  # type: ignore[arg-type]
        submission_id=submission.id,  # type: ignore[arg-type]
        created_problem=created_problem,
    )


@router.get("/get-solved-questions", response_model=GetSolvedQuestionsResponse)
def get_solved_questions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Get all problems for the current user with their first submission date
    stmt = (
        select(
            Problem.id,
            Problem.leetcode_slug,
            Problem.problem_title,
            Problem.attempts,
            func.min(Submission.createdat).label("first_solved_date")
        )
        .join(Submission, Problem.id == Submission.problem_id)
        .where(Problem.user_id == current_user.username)
        .group_by(Problem.id, Problem.leetcode_slug, Problem.problem_title, Problem.attempts)
        .order_by(func.min(Submission.createdat).desc())
    )
    
    rows = session.exec(stmt).all()
    items: List[SolvedQuestion] = []
    for row in rows:
        items.append(
            SolvedQuestion(
                problem_id=row.id,
                leetcode_slug=row.leetcode_slug,
                problem_title=row.problem_title,
                first_solved_date=row.first_solved_date,
                attempts=row.attempts,
            )
        )
    
    return GetSolvedQuestionsResponse(items=items)


