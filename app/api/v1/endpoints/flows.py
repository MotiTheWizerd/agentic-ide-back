from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.dependency import get_db
from app.models.flow import Flow
from app.api.v1.schemas.flow import FlowSave, FlowResponse, FlowLoadRequest, FlowRecord

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("/save-flow", response_model=FlowResponse)
async def save_flow(body: FlowSave, db: AsyncSession = Depends(get_db)):
    graph_data = {
        "nodes": body.nodes,
        "edges": body.edges,
        "providerId": body.providerId,
    }

    existing = await db.get(Flow, body.id)

    if existing:
        existing.name = body.name
        existing.graph_data = graph_data
    else:
        existing = Flow(
            id=body.id,
            name=body.name,
            user_id=body.user_id,
            project_id=body.project_id,
            graph_data=graph_data,
        )
        db.add(existing)

    await db.commit()
    await db.refresh(existing)
    return existing


@router.post("/load-flows", response_model=List[FlowRecord])
async def load_flows(body: FlowLoadRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Flow).where(
            Flow.user_id == body.user_id,
            Flow.project_id == body.project_id,
        )
    )
    return result.scalars().all()
