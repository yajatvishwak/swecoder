from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.services.auth import (
    authenticate_user,
    create_access_token,
    decode_token,
    get_password_hash,
    revoke_token,
    is_token_revoked,
)
from app.models.user import User
from app.schemas.user import (
    SignupRequest,
    SignupResponse,
    VerifyTokenRequest,
    VerifyTokenResponse,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(user.username, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(token: str, session: Annotated[Session, Depends(get_session)]):
    # Expect raw bearer token from client for simplicity
    try:
        payload = decode_token(token)
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=400, detail="Invalid token")
        revoke_token(session, jti)
        return {"detail": "Logged out"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")



@router.post("/signup", response_model=SignupResponse)
def signup(payload: SignupRequest, session: Annotated[Session, Depends(get_session)]):
    # Ensure username is unique
    existing = session.get(User, payload.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Create user with hashed password
    user = User(
        username=payload.username,
        password=get_password_hash(payload.password),
        name=payload.name,
    )
    session.add(user)
    session.commit()
    # Ensure the user instance is synced from DB
    session.refresh(user)

    access_token = create_access_token(user.username, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return SignupResponse(access_token=access_token, token_type="bearer")


@router.post("/verify", response_model=VerifyTokenResponse)
def verify(payload: VerifyTokenRequest, session: Annotated[Session, Depends(get_session)]):
    try:
        token_payload = decode_token(payload.token)
        jti = token_payload.get("jti")
        if not jti or is_token_revoked(session, jti):
            return VerifyTokenResponse(valid=False)
        return VerifyTokenResponse(valid=True)
    except JWTError:
        return VerifyTokenResponse(valid=False)

