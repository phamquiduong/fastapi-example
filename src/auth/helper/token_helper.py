from datetime import datetime

from auth.constants.token_constant import TokenType
from auth.models.user_model import UserModel
from auth.schemas.token_schema import TokenSchema
from core.error import ErrorCode, FastAPIException
from core.helper.jwt_helper import JWTHelper
from core.settings import settings


class TokenHelperBase:
    token_type: TokenType
    exp: datetime

    def render_token(self, user: UserModel):
        return JWTHelper.encode({
            'sub': {
                'user_id': user.id,
            },
            'type': self.token_type,
            'exp': self.exp,
        })

    def auth_token(self, token: str):
        payload = JWTHelper.decode(token)

        if payload.get('type', None) != self.token_type:
            raise FastAPIException(ErrorCode.AUTH_4011, detail=f'Token type must be {self.token_type.value}')

        try:
            return int(payload.get('sub', {}).get('user_id', None))
        except Exception as error:
            raise FastAPIException(ErrorCode.JWT_5002, detail=str(error)) from error

    def fetch_token_response(self, user: UserModel) -> TokenSchema:
        return TokenSchema(
            token=self.render_token(user),
            type=self.token_type,
            exp=self.exp
        )


# Authentication token class
class AccessTokenHelper(TokenHelperBase):
    token_type = TokenType.ACCESS
    exp = settings.access_token_exp + datetime.now()


class RefreshTokenHelper(TokenHelperBase):
    token_type = TokenType.REFRESH
    exp = settings.refresh_token_exp+datetime.now()
