import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, Uuid, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class OutputType(str, PyEnum):
    text = "text"
    image = "image"
    persona_name = "persona_name"
    persona_description = "persona_description"


class ComponentOutputSchema(Base):
    __tablename__ = "component_output_schema"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    component_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("agentic_components.id"), index=True
    )
    output_key: Mapped[str] = mapped_column(String(100))
    output_type: Mapped[OutputType] = mapped_column(
        Enum(OutputType, native_enum=False, length=25)
    )
    source: Mapped[str] = mapped_column(String(255))
