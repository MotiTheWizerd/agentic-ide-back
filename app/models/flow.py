import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Integer, Uuid, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Flow(Base):
    __tablename__ = "flows"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True
    )
    project_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True, index=True
    )
    graph_data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
