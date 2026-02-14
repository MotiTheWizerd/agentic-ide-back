from pydantic import BaseModel

from app.api.v1.schemas.user import UserResponse


class LoginRequest(BaseModel):
    identifier: str  # email or username
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshRequest(BaseModel):
    refresh_token: str
