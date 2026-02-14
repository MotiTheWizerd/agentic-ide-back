"""REST endpoint for triggering graph execution."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.di.registry import registry
from app.modules.execution.manager import ExecutionManager

router = APIRouter(prefix="/execution", tags=["execution"])


class ExecutionRequest(BaseModel):
    flow_id: str
    nodes: list[dict]
    edges: list[dict]
    provider_id: str
    trigger_node_id: str | None = None
    cached_outputs: dict[str, dict] | None = None


class ExecutionResponse(BaseModel):
    run_id: str


@router.post("/run", response_model=ExecutionResponse)
async def run_execution(
    body: ExecutionRequest,
    current_user=Depends(get_current_user),
    manager: ExecutionManager = Depends(registry.get(ExecutionManager)),
):
    """Start a graph execution run.

    Returns the ``run_id`` immediately. Real-time status updates are
    delivered via WebSocket events.
    """
    run_id = await manager.run(
        user_id=current_user.id,
        flow_id=body.flow_id,
        nodes=body.nodes,
        edges=body.edges,
        provider_id=body.provider_id,
        trigger_node_id=body.trigger_node_id,
        cached_outputs=body.cached_outputs,
    )
    return ExecutionResponse(run_id=run_id)
