from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    project_name: str
    user_id: int


class ProjectSelectByUser(BaseModel):
    user_id: int


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
