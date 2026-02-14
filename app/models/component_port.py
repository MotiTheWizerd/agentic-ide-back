import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, Boolean, Integer, Uuid, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class PortDirection(str, PyEnum):
    in_ = "in"
    out = "out"


class PortType(str, PyEnum):
    text = "text"
    adapter = "adapter"


class ComponentPort(Base):
    __tablename__ = "component_ports"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    component_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("agentic_components.id"), index=True
    )
    direction: Mapped[PortDirection] = mapped_column(
        Enum(PortDirection, native_enum=False, length=5)
    )
    port_type: Mapped[PortType] = mapped_column(
        Enum(PortType, native_enum=False, length=10)
    )
    handle_id: Mapped[str] = mapped_column(String(100))
    max_connections: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    is_dynamic: Mapped[bool] = mapped_column(Boolean, default=False)
    max_dynamic: Mapped[int] = mapped_column(Integer, default=5)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
