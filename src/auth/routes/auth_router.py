from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.helper.auth_helper import AuthHelper
from auth.helper.token_helper import AccessTokenHelper, RefreshTokenHelper
from auth.helper.user_helper import UserHelper
from auth.schemas.token_schema import (AuthTokenSchema,
                                       OAuth2PasswordBearerTokenSchema)
from auth.schemas.user_schema import (UserInSchema, UserLoginSchema,
                                      UserOutSchema)
from core.dependencies.db_depend import get_session
from core.schemas.error_schema import ErrorSchema, FieldErrorSchema

auth_route = APIRouter(tags=['Authentication'])


@auth_route.post('/token', include_in_schema=False,
                 response_model=OAuth2PasswordBearerTokenSchema)
def oauth2_token(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = AuthHelper(session).by_email_password(email=form.username, password=form.password)
    return {'access_token': AccessTokenHelper().render_token(user)}


@auth_route.post('/register',
                 status_code=status.HTTP_201_CREATED,
                 response_model=UserOutSchema,
                 responses={
                     422: {'model': FieldErrorSchema},
                     500: {'model': ErrorSchema}})
def user_register(
    user_in: UserInSchema = Body(...),
    session: Session = Depends(get_session)
):
    user_db = UserHelper(session).create_user(user_in)
    return UserOutSchema(**user_db.__dict__)


@auth_route.post('/login', response_model=AuthTokenSchema,
                 responses={
                     422: {'model': FieldErrorSchema},
                     500: {'model': ErrorSchema}})
def user_login(
    user_login_form: UserLoginSchema = Body(...),
    session: Session = Depends(get_session)
):
    user = AuthHelper(session).by_email_password(email=user_login_form.email, password=user_login_form.password)
    return AuthTokenSchema(
        access_token=AccessTokenHelper().fetch_token_response(user=user),
        refresh_token=RefreshTokenHelper().fetch_token_response(user=user)
    )


@auth_route.post('/refresh', response_model=AuthTokenSchema,
                 responses={
                     422: {'model': FieldErrorSchema},
                     500: {'model': ErrorSchema}})
def user_refresh_token(
    refresh_token: str = Body(..., embed=True),
    session: Session = Depends(get_session)
):
    user = AuthHelper(session).by_token(token=refresh_token, helper=RefreshTokenHelper())
    return AuthTokenSchema(
        access_token=AccessTokenHelper().fetch_token_response(user=user),
        refresh_token=RefreshTokenHelper().fetch_token_response(user=user)
    )
