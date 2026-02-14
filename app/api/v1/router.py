from fastapi import APIRouter

from app.core.di.discovery import discover_routers

router = APIRouter(prefix="/api/v1")

for _r in discover_routers("app.api.v1.endpoints"):
    router.include_router(_r)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
