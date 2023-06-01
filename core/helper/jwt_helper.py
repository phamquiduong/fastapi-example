"""JWT token helper module"""

import jwt
from fastapi import HTTPException, status

from core.constants import ALGORITHM, SECRET_KEY


class JWTHelper:
    """JWT helper class
    Using secret key and algorithm from environment variables

    Methods:
        encode (class method): Encode the payload and return the token string
        decode (class method): Decode the token string and return payload
    """

    secret_key = SECRET_KEY
    algorithm = ALGORITHM

    @classmethod
    def encode(cls, payload: dict) -> str:
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
                              key=cls.secret_key,
                              algorithm=cls.algorithm)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)) from error

    @classmethod
    def decode(cls, token: str) -> dict:
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
                              key=cls.secret_key,
                              algorithms=cls.algorithm)
        except jwt.ExpiredSignatureError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Bearer"},
                                detail='Signature expired') from error
        except jwt.InvalidTokenError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Bearer"},
                                detail='Invalid token') from error


jwt_helper = JWTHelper()
