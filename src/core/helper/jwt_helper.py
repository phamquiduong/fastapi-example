import jwt
from fastapi import HTTPException, status

from core.settings import settings


class __JWTHelper:
    """JWT helper private class
    Args:
        secret_key (str): Secret key
        algorithm (str): Algorithm

    Methods:
        encode (class method): Encode the payload and return the token string
        decode (class method): Decode the token string and return payload
    """

    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.__secret_key = secret_key
        self.__algorithm = algorithm

    def encode(self, payload: dict) -> str:
        """Encoding JWT function.

        Args:
            payload (dict): Payload of JWT token. Example:
            ```json
            {"user_id": 1, "exp": "20230606 10:43:23"}
            ```

        Raises:
            HTTPException: Encode error message. Status code 500

        Returns:
            str: JWT token base on payload
        """
        try:
            return jwt.encode(payload=payload,
                              key=self.__secret_key,
                              algorithm=self.__algorithm)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)) from error

    def decode(self, token: str) -> dict:
        """Decode JWT token

        Args:
            token (str): JWT token

        Raises:
            HTTPException: Signature exprired. status code 401
            HTTPException: Invalid token, status code 401

        Returns:
            dict: Payload of JWT token
        """
        try:
            return jwt.decode(jwt=token,
                              key=self.__secret_key,
                              algorithms=self.__algorithm)
        except jwt.ExpiredSignatureError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Bearer"},
                                detail='Signature expired') from error
        except jwt.InvalidTokenError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Bearer"},
                                detail='Invalid token') from error


jwt_helper = __JWTHelper(
    secret_key=settings.secret_key,
    algorithm=settings.algorithm
)
