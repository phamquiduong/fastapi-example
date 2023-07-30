from pydantic import BaseModel, ConfigDict


class ErrorField(BaseModel):
    field: str
    detail: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "field": "email",
            "detail": "value is not a valid email address: There must be something after the @-sign."}})


class ErrorSchema(BaseModel):
    error_code: str
    error_message: str
    error_detail: str | None = None

    error_fields: list[ErrorField] | None = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "error_code": "ERR_500",
            "error_message": "Internal server error",
            "error_detail": "Division by zero"}})


class FieldErrorSchema(ErrorSchema):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "error_code": "ERR_422",
            "error_message": "Request validation error",
            "error_fields": [{
                "field": "email",
                "detail": "value is not a valid email address: There must be something after the @-sign."}]}})
