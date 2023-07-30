import jwt

from core.error import ErrorCode, FastAPIException
from core.settings import settings


class JWTHelper:
    @staticmethod
    def encode(payload: dict) -> str:
        try:
            return jwt.encode(payload=payload,
                              key=settings.secret_key,
                              algorithm=settings.algorithm)
        except Exception as error:
            raise FastAPIException(ErrorCode.JWT_5001, detail=str(error)) from error

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(jwt=token,
                              key=settings.secret_key,
                              algorithms=[settings.algorithm])
        except jwt.ExpiredSignatureError as error:
            raise FastAPIException(ErrorCode.JWT_4011) from error
        except jwt.InvalidTokenError as error:
            raise FastAPIException(ErrorCode.JWT_4012) from error
        except Exception as error:
            raise FastAPIException(ErrorCode.JWT_5002) from error
