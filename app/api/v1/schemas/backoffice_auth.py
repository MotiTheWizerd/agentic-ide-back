from datetime import datetime

from pydantic import BaseModel


class BackofficeLoginRequest(BaseModel):
    identifier: str  # email or username
    password: str


class BackofficeTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class BackofficeUserCreate(BaseModel):
    username: str
    email: str
    password: str


class BackofficeUserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
