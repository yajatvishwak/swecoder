from typing import Optional

from sqlmodel import SQLModel


class SignupRequest(SQLModel):
    username: str
    password: str
    name: Optional[str] = None


class SignupResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"


class VerifyTokenRequest(SQLModel):
    token: str


class VerifyTokenResponse(SQLModel):
    valid: bool



