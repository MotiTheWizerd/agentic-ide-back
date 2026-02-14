import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, Boolean, Integer, Uuid, Enum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class FieldType(str, PyEnum):
    text = "text"
    textarea = "textarea"
    select = "select"
    number = "number"
    image = "image"
    tags = "tags"


class ComponentField(Base):
    __tablename__ = "component_fields"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    component_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("agentic_components.id"), index=True
    )
    field_key: Mapped[str] = mapped_column(String(100))
    label: Mapped[str] = mapped_column(String(255))
    field_type: Mapped[FieldType] = mapped_column(
        Enum(FieldType, native_enum=False, length=20)
    )
    placeholder: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    default_value: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    required: Mapped[bool] = mapped_column(Boolean, default=False)
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    validation: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
