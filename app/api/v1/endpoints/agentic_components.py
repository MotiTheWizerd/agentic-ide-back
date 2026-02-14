from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.dependency import get_db
from app.models.agentic_component import AgenticComponent
from app.api.v1.schemas.agentic_component import ComponentSidebarItem

router = APIRouter(prefix="/components", tags=["components"])


@router.post("/get-components", response_model=List[ComponentSidebarItem])
async def get_all_components(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AgenticComponent).where(AgenticComponent.is_active == True)
    )
    return result.scalars().all()
