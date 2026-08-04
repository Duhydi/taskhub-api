from typing import Any

from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "detail": "Permission denied",
                }
            ]
        }
    )


class ValidationErrorItem(BaseModel):
    loc: list[str | int]
    msg: str
    type: str
    input: Any | None = None


class ValidationErrorResponse(BaseModel):
    detail: list[ValidationErrorItem]