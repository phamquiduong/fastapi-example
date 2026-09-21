from typing import Any

from fastapi import status
from pydantic import BaseModel, ConfigDict


class FieldError(BaseModel):
    name: str
    message: str
    type: str
    input: Any
    context: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    status: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Bad Request."
    fields: list[FieldError] | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": 422,
                "detail": "Unprocessable Content.",
                "fields": [
                    {
                        "name": "email",
                        "message": "value is not a valid email address: An email address must have an @-sign.",
                        "type": "value_error",
                        "input": "user",
                        "context": {"reason": "An email address must have an @-sign."},
                    },
                    {
                        "name": "password",
                        "message": "Password does not match the regex.",
                        "type": "not_match_regex",
                        "input": "12373854",
                        "context": {"regex": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9]).{8,64}$"},
                    },
                ],
            }
        }
    )
