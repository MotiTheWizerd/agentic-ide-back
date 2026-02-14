from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class FlowSave(BaseModel):
    id: UUID
    name: str
    user_id: int
    project_id: int | None = None
    nodes: list[Any]
    edges: list[Any]
    providerId: str | None = None
    updatedAt: int | None = None
    createdAt: int | None = None


class FlowLoadRequest(BaseModel):
    user_id: int
    project_id: int


class FlowRecord(BaseModel):
    id: UUID
    name: str
    graph_data: dict
    updated_at: datetime

    model_config = {"from_attributes": True}


class FlowResponse(BaseModel):
    id: UUID
    name: str
    user_id: int
    project_id: int | None
    graph_data: dict
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
