from datetime import datetime

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    token: str
    exp: datetime


class AuthToken(BaseModel):
    access_token: Token
    refresh_token: Token


class TokenData(BaseModel):
    email: EmailStr


class OAuth2PasswordBearerToken(BaseModel):
    access_token: str
    token_type: str
