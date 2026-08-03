from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.task_enum import (
    TaskPriority,
    TaskStatus,
)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM

    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

    status: TaskStatus
    priority: TaskPriority

    assignee_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str

    status: TaskStatus
    priority: TaskPriority

    created_by: int
    assignee_id: int | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )