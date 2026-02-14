from pydantic import BaseModel, Field


class WSMessage(BaseModel):
    type: str
    data: dict = Field(default_factory=dict)
