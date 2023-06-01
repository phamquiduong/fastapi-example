from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from auth.helper.helper import authenticate_user
from auth.helper.token_helper import AccessTokenHelper, RefreshTokenHelper
from auth.schemas import AuthToken, OAuth2PasswordBearerToken, Token
from core.constants import DEFAULT_ROLE
from core.dependencies import get_db
from users import schemas as user_schemas
from users.crud import create_user, get_user

auth_route = APIRouter(tags=['Authentication'])


@auth_route.post('/token', response_model=OAuth2PasswordBearerToken, include_in_schema=False)
def oauth2_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    user = authenticate_user(db, email=email, password=password)
    access_token_helper = AccessTokenHelper()

    return {"access_token": access_token_helper.render_token(user), "token_type": "bearer"}


@auth_route.post('/register', status_code=status.HTTP_201_CREATED, response_model=user_schemas.User)
def user_register(
    user_create: Annotated[user_schemas.UserCreate, Body(...)],
    db: Session = Depends(get_db)
):
    if get_user(db, email=user_create.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already registered')
    return create_user(db, user_create, DEFAULT_ROLE).__dict__


@auth_route.post('/login', response_model=AuthToken)
def user_login(
    email: Annotated[EmailStr, Body(...)],
    password: Annotated[str, Body(...)],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email=email, password=password)

    access_token_helper = AccessTokenHelper()
    refresh_token_helper = RefreshTokenHelper()

    return AuthToken(
        access_token=Token(token=access_token_helper.render_token(user), exp=access_token_helper.exp),
        refresh_token=Token(token=refresh_token_helper.render_token(user), exp=refresh_token_helper.exp)
    )


@auth_route.post('/refresh', response_model=AuthToken)
def user_refresh_token(
    refresh_token: Annotated[str, Body(...)],
    db: Session = Depends(get_db)
):
    access_token_helper = AccessTokenHelper()
    refresh_token_helper = RefreshTokenHelper()

    user_id = refresh_token_helper.auth_token(token=refresh_token)
    user = get_user(db, user_id=user_id)

    return AuthToken(
        access_token=Token(token=access_token_helper.render_token(user), exp=access_token_helper.exp),
        refresh_token=Token(token=refresh_token_helper.render_token(user), exp=refresh_token_helper.exp)
    )
