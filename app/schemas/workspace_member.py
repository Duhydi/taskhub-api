from pydantic import BaseModel

from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)


class WorkspaceMemberCreate(BaseModel):
    user_id: int
    role: WorkspaceMemberRole


class WorkspaceMemberResponse(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: WorkspaceMemberRole

    model_config = {
        "from_attributes": True,
    }