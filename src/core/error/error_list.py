from enum import Enum

from fastapi import status

from core.schemas.error_schema import ErrorSchema


class ErrorCode(Enum):
    # FastAPI exception
    ERR_401 = "Not authenticated", status.HTTP_401_UNAUTHORIZED
    ERR_422 = 'Request validation error', status.HTTP_422_UNPROCESSABLE_ENTITY
    ERR_500 = 'Internal server error', status.HTTP_500_INTERNAL_SERVER_ERROR

    # JWT exception
    JWT_5001 = 'JWT encode error', status.HTTP_500_INTERNAL_SERVER_ERROR
    JWT_5002 = 'JWT decode error', status.HTTP_500_INTERNAL_SERVER_ERROR
    JWT_4011 = 'Signature expired', status.HTTP_401_UNAUTHORIZED
    JWT_4012 = 'Invalid token', status.HTTP_401_UNAUTHORIZED

    # Database exception
    DB_5001 = 'Database error', status.HTTP_500_INTERNAL_SERVER_ERROR

    # Authentication exception
    AUTH_4011 = 'Token type invalid', status.HTTP_401_UNAUTHORIZED
    AUTH_4012 = 'User is not found', status.HTTP_401_UNAUTHORIZED
    AUTH_4013 = 'Password is incorrect', status.HTTP_401_UNAUTHORIZED
    AUTH_4014 = 'Inactive user', status.HTTP_401_UNAUTHORIZED
    AUTH_4091 = 'User already exist', status.HTTP_409_CONFLICT

    def get_response(self) -> tuple[ErrorSchema, int]:
        return ErrorSchema(
            error_code=self.name,
            error_message=self.value[0]
        ), self.value[1]
