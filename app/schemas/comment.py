from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CommentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1000,
    )


class CommentUpdate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1000,
    )


class CommentResponse(BaseModel):
    id: int
    task_id: int
    author_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )