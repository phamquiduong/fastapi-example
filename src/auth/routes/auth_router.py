from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.crud.user_crud import create_user, get_user
from auth.helper.auth_helper import authenticate_user
from auth.schemas.token_schema import (AuthTokenSchema,
                                       OAuth2PasswordBearerTokenSchema)
from auth.schemas.user_schema import (UserInSchema, UserLoginSchema,
                                      UserOutSchema)
from core.constants.token_constant import TOKEN_EXAMPLE
from core.dependencies.db_depend import get_session
from core.helper.token_helper import access_token_helper, refresh_token_helper
from core.schemas.error_schema import (HTTPExceptionSchema,
                                       RequestValidationErrorSchema)

auth_route = APIRouter(tags=['Authentication'])


@auth_route.post('/token', include_in_schema=False,
                 response_model=OAuth2PasswordBearerTokenSchema,
                 responses={
                     200: {'model': OAuth2PasswordBearerTokenSchema},
                     401: {'model': HTTPExceptionSchema},
                     422: {'model': RequestValidationErrorSchema},
                     500: {'model': HTTPExceptionSchema},
                 })
def oauth2_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    email = form_data.username
    password = form_data.password

    user = authenticate_user(session, email=email, password=password)

    return {'access_token': access_token_helper.render_token(user)}


@auth_route.post('/register',
                 status_code=status.HTTP_201_CREATED,
                 response_model=UserOutSchema,
                 responses={
                     201: {'model': UserOutSchema},
                     409: {'model': HTTPExceptionSchema},
                     422: {'model': RequestValidationErrorSchema},
                     500: {'model': HTTPExceptionSchema},
                 })
def user_register(
    user_create: Annotated[UserInSchema, Body(...)],
    session: Session = Depends(get_session)
):
    return create_user(session, user_create).__dict__


@auth_route.post('/login', response_model=AuthTokenSchema,
                 responses={
                     200: {'model': AuthTokenSchema},
                     401: {'model': HTTPExceptionSchema},
                     422: {'model': RequestValidationErrorSchema},
                     500: {'model': HTTPExceptionSchema},
                 })
def user_login(
    user: UserLoginSchema = Body(...),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, email=user.email, password=user.password)

    return {
        'access_token': {'token': access_token_helper.render_token(user)},
        'refresh_token': {'token': refresh_token_helper.render_token(user)}
    }


@auth_route.post('/refresh', response_model=AuthTokenSchema,
                 responses={
                     401: {'model': HTTPExceptionSchema},
                     404: {'model': HTTPExceptionSchema},
                     422: {'model': RequestValidationErrorSchema},
                     500: {'model': HTTPExceptionSchema},
                 })
def user_refresh_token(
    refresh_token: Annotated[str, Body(..., example=TOKEN_EXAMPLE)],
    session: Session = Depends(get_session)
):
    user_id = refresh_token_helper.auth_token(token=refresh_token)
    user = get_user(session, user_id=user_id)

    return {
        'access_token': {'token': access_token_helper.render_token(user)},
        'refresh_token': {'token': refresh_token_helper.render_token(user)}
    }
