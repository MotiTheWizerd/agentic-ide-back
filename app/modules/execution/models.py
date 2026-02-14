from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class NodeStatus(str, Enum):
    IDLE = "idle"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"
    SKIPPED = "skipped"


class ExecutionStep(BaseModel):
    node_id: str
    node_type: str
    input_node_ids: list[str] = Field(default_factory=list)
    adapter_node_ids: list[str] = Field(default_factory=list)


class NodeOutput(BaseModel):
    text: str | None = None
    image: str | None = None
    persona_description: str | None = None
    persona_name: str | None = None
    replace_prompt: str | None = None
    injected_prompt: str | None = None
    error: str | None = None
    duration_ms: float | None = None


class NodeExecutionContext(BaseModel):
    node_id: str
    node_type: str
    node_data: dict
    text_inputs: list[NodeOutput] = Field(default_factory=list)
    adapter_inputs: list[NodeOutput] = Field(default_factory=list)
    provider_id: str = ""
    model: str = ""
    temperature: float = 0.7
    run_id: str = ""
    user_id: int = 0


class ResolvedModel(BaseModel):
    provider_id: str
    model: str
    temperature: float = 0.7


class ExecutionRequest(BaseModel):
    flow_id: str
    nodes: list[dict]
    edges: list[dict]
    provider_id: str
    trigger_node_id: str | None = None
    cached_outputs: dict[str, dict] | None = None
