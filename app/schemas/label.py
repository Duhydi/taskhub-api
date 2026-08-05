from pydantic import BaseModel, ConfigDict, Field


class LabelCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )

    color: str = Field(
        min_length=1,
        max_length=20,
    )


class LabelUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    color: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )


class LabelResponse(BaseModel):
    id: int
    project_id: int
    name: str
    color: str

    model_config = ConfigDict(
        from_attributes=True,
    )