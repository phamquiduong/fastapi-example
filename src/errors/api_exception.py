from fastapi import HTTPException, status

from schemas.error import FieldError


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Bad Request.",
        headers: dict[str, str] | None = None,
        fields: FieldError | list[FieldError] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.fields = [fields] if isinstance(fields, FieldError) else fields

    def __str__(self) -> str:
        return f"Detail: {self.detail} - Fields: {self.fields}"
