from fastapi import FastAPI

from app.core.config import settings
from app.db.init_db import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.submissions import router as submissions_router
from app.api.v1.revisions import router as revisions_router
from app.api.v1.activity import router as activity_router


app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(submissions_router, prefix="/api/v1")
app.include_router(revisions_router, prefix="/api/v1")
app.include_router(activity_router, prefix="/api/v1")


