import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, Integer, Uuid, Enum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ExecutorType(str, PyEnum):
    api_call = "api_call"
    data_source = "data_source"
    pass_through = "pass_through"
    composite = "composite"


class ComponentApiConfig(Base):
    __tablename__ = "component_api_config"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    component_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("agentic_components.id"), index=True
    )
    api_route: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    request_mapping: Mapped[dict] = mapped_column(JSON)
    response_mapping: Mapped[dict] = mapped_column(JSON)
    pass_through_condition: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    compression_threshold: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    executor_type: Mapped[ExecutorType] = mapped_column(
        Enum(ExecutorType, native_enum=False, length=20)
    )
