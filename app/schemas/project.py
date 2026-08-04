from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.project import ProjectStatus


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    workspace_id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }