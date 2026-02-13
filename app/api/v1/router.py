from fastapi import APIRouter

from app.api.v1.endpoints import users, projects, auth

router = APIRouter(prefix="/api/v1")
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(projects.router)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
