from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from pydantic import BaseModel

from app.db.session import get_session
from app.models.submission import Submission
from app.models.user import User
from app.services.auth import get_current_user


router = APIRouter(prefix="", tags=["activity"])


class ActivityData(BaseModel):
    submissions: int
    revisions: int


class GetActivityResponse(BaseModel):
    data: Dict[str, ActivityData]


@router.get("/get-activity", response_model=GetActivityResponse)
def get_activity(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get daily activity data (submissions and revisions) for the heatmap.
    Returns a dictionary with dates as keys and activity counts as values.
    """
    # Get all non-revision submissions for the user, grouped by date
    submissions_stmt = (
        select(
            func.date(Submission.createdat).label("date"),
            func.count(Submission.id).label("count")
        )
        .where(
            (Submission.user_id == current_user.username) &
            (Submission.is_revision == False)  # type: ignore
        )
        .group_by(func.date(Submission.createdat))
    )
    
    submissions_result = session.exec(submissions_stmt).all()
    
    # Get all revision submissions for the user, grouped by date
    revisions_stmt = (
        select(
            func.date(Submission.createdat).label("date"),
            func.count(Submission.id).label("count")
        )
        .where(
            (Submission.user_id == current_user.username) &
            (Submission.is_revision == True)  # type: ignore
        )
        .group_by(func.date(Submission.createdat))
    )
    
    revisions_result = session.exec(revisions_stmt).all()
    
    # Build the response dictionary
    activity_data: Dict[str, ActivityData] = {}
    
    # Add submissions
    for row in submissions_result:
        date_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
        activity_data[date_str] = ActivityData(submissions=row.count, revisions=0)
    
    # Add revisions
    for row in revisions_result:
        date_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
        if date_str in activity_data:
            activity_data[date_str].revisions = row.count
        else:
            activity_data[date_str] = ActivityData(submissions=0, revisions=row.count)
    
    return GetActivityResponse(data=activity_data)

