from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict = Field(default_factory=dict)
