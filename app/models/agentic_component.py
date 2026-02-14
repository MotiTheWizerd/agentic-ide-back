import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import String, Text, DateTime, Boolean, Integer, Uuid, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ComponentCategory(str, PyEnum):
    input = "input"
    processing = "processing"
    output = "output"
    data_source = "data_source"
    utility = "utility"


class ProviderType(str, PyEnum):
    text = "text"
    image = "image"
    vision = "vision"
    none = "none"


class AgenticComponent(Base):
    __tablename__ = "agentic_components"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    type: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[ComponentCategory] = mapped_column(
        Enum(ComponentCategory, native_enum=False, length=20)
    )
    icon: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(50))
    uses_llm: Mapped[bool] = mapped_column(Boolean, default=False)
    default_provider_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    default_model: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    provider_type: Mapped[ProviderType] = mapped_column(
        Enum(ProviderType, native_enum=False, length=10)
    )
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
