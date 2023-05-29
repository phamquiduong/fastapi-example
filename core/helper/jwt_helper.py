import jwt
from fastapi import HTTPException, status

from core.constants import ALGORITHM, SECRET_KEY


class JWTHelper:
    secret_key = SECRET_KEY
    algorithm = ALGORITHM

    @classmethod
    def encode(cls, payload: dict) -> str:
        try:
            return jwt.encode(payload=payload,
                              key=cls.secret_key,
                              algorithm=cls.algorithm)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(jwt=token,
                              key=cls.secret_key,
                              algorithms=cls.algorithm)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Bearer"},
                                detail='Signature_expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Bearer"},
                                detail='Invalid_token')


jwt_helper = JWTHelper()
