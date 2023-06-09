from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import HTTPException, status

from core.constants import ACCESS_TOKEN_EXP, REFRESH_TOKEN_EXP
from core.helper.jwt_helper import jwt_helper
from users import models as user_models


# Base class for authentication token
class BaseTokenHelper(ABC):
    @classmethod
    @abstractmethod
    def render_token(cls, user: user_models.User) -> str:
        """Render the authorization token for the given user

        Args:
            user (user_models.User): user model match with database connection

        Returns:
            str: authorization token
        """
        ...

    @classmethod
    @abstractmethod
    def auth_token(cls, token: str) -> int:
        """Authenticate the given token

        Args:
            token (str): authorization token

        Returns:
            int: authorization user_id
        """
        ...


################################################################
# Authentication token class
################################################################
class AccessTokenHelper(BaseTokenHelper):
    token_type = 'access'
    exp = datetime.now() + ACCESS_TOKEN_EXP

    @classmethod
    def render_token(cls, user: user_models.User):
        return _render_token(user, cls.token_type, cls.exp)

    @classmethod
    def auth_token(cls, token: str):
        return _get_payload(token, cls.token_type)


class RefreshTokenHelper(BaseTokenHelper):
    token_type = 'refresh'
    exp = datetime.now() + REFRESH_TOKEN_EXP

    @classmethod
    def render_token(cls, user: user_models.User):
        return _render_token(user, cls.token_type, cls.exp)

    @classmethod
    def auth_token(cls, token: str):
        return _get_payload(token, cls.token_type)


################################################################
# Helper function
################################################################
def _get_payload(token: str, token_type: str) -> str:
    payload = jwt_helper.decode(token)

    if payload.get('sub', {}).get('type', None) != token_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token type mismatch')

    return payload.get('sub', {}).get('user_id', None)


def _render_token(user: user_models.User, token_type: str, exp: datetime) -> str:
    return jwt_helper.encode({
        'sub': {
            'user_id': user.id,
            'type': token_type,
        },
        'exp': exp,
    })
