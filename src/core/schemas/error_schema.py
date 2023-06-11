from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "I'm sorry.. It is an error.."},
        }


class FieldErrorSchema(BaseModel):
    name: str
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "name": "field1",
                "detail": "value is not a valid email address"
            },
        }


class RequestValidationErrorSchema(BaseModel):
    detail: str = 'Request validation error'
    fields: list[FieldErrorSchema] = []

    class Config:
        schema_extra = {
            "example": {
                "detail": "Request validation error",
                "fields": [
                    {
                        "name": "field1",
                        "detail": "value is not a valid email address"
                    },
                    {
                        "name": "field2",
                        "detail": "field required"
                    }
                ]
            },
        }
