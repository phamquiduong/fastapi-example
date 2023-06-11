from pydantic import BaseModel

from core.constants.token_constant import TOKEN_EXAMPLE


class TokenSchema(BaseModel):
    token: str
    type: str = "bearer"

    class Config:
        schema_extra = {
            "example": {
                "token": TOKEN_EXAMPLE,
                "type": "bearer"
            },
        }


class AuthTokenSchema(BaseModel):
    access_token: TokenSchema
    refresh_token: TokenSchema


class OAuth2PasswordBearerTokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        schema_extra = {
            "example": {
                "access_token": TOKEN_EXAMPLE,
                "type": "bearer"
            },
        }
