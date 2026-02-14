from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.dependency import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.backoffice_user import BackofficeUser
from app.api.v1.schemas.backoffice_auth import (
    BackofficeLoginRequest,
    BackofficeTokenResponse,
    BackofficeUserCreate,
    BackofficeUserResponse,
)

router = APIRouter(prefix="/auth/backoffice", tags=["backoffice-auth"])


@router.post("/create", response_model=BackofficeUserResponse, status_code=201)
async def create_backoffice_user(body: BackofficeUserCreate, db: AsyncSession = Depends(get_db)):
    user = BackofficeUser(
        username=body.username,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=BackofficeTokenResponse)
async def backoffice_login(body: BackofficeLoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BackofficeUser).where(
            or_(BackofficeUser.email == body.identifier, BackofficeUser.username == body.identifier)
        )
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return BackofficeTokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
