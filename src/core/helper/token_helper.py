from datetime import datetime, timedelta

from fastapi import HTTPException, status

from auth.models.user_role_model import UserModel
from core.helper.jwt_helper import jwt_helper
from core.settings import settings


# Base class for authentication token
class __TokenHelperBase:
    token_type: str
    exp: timedelta

    def render_token(self, user: UserModel):
        return jwt_helper.encode({
            'sub': {
                'user_id': user.id,
                'type': self.token_type,
            },
            'exp': datetime.now() + self.exp,
        })

    def auth_token(self, token: str):
        payload = jwt_helper.decode(token)

        if payload.get('sub', {}).get('type', None) != self.token_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'Token type must be {self.token_type}')

        return int(payload.get('sub', {}).get('user_id', None))


# Authentication token class
class __AccessTokenHelper(__TokenHelperBase):
    token_type = 'access'
    exp = settings.access_token_exp


class __RefreshTokenHelper(__TokenHelperBase):
    token_type = 'refresh'
    exp = settings.refresh_token_exp


# Instance of Authentication token helper
access_token_helper = __AccessTokenHelper()
refresh_token_helper = __RefreshTokenHelper()
