from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from auth.crud.user_crud import delete_user, update_user
from auth.dependencies.auth_depend import get_current_active_user
from auth.models.user_role_model import UserModel
from auth.schemas.role_schema import RoleOutSchema
from auth.schemas.user_schema import UserOutSchema, UserUpdateSchema
from core.dependencies.db_depend import get_session
from core.schemas.error_schema import (HTTPExceptionSchema,
                                       RequestValidationErrorSchema)

user_route = APIRouter(prefix='/user', tags=['User'])


@user_route.get('', response_model=UserOutSchema,
                responses={
                    401: {'model': HTTPExceptionSchema},
                    404: {'model': HTTPExceptionSchema},
                    500: {'model': HTTPExceptionSchema},
                })
def get_current_user(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user.__dict__


@user_route.put('', response_model=UserOutSchema,
                responses={
                    401: {'model': HTTPExceptionSchema},
                    404: {'model': HTTPExceptionSchema},
                    422: {'model': RequestValidationErrorSchema},
                    500: {'model': HTTPExceptionSchema},
                })
def update_current_user(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    user: Annotated[UserUpdateSchema, Body(...)],
    session: Session = Depends(get_session)
):
    return update_user(session, user_db=current_user, user=user).__dict__


@user_route.delete('', status_code=status.HTTP_204_NO_CONTENT,
                   responses={
                       401: {'model': HTTPExceptionSchema},
                       404: {'model': HTTPExceptionSchema},
                       500: {'model': HTTPExceptionSchema},
                   })
def remove_current_user(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    delete_user(session=session, user_db=current_user)


@user_route.get('/role', response_model=list[RoleOutSchema],
                responses={
                    401: {'model': HTTPExceptionSchema},
                    404: {'model': HTTPExceptionSchema},
                    500: {'model': HTTPExceptionSchema},
})
def get_current_user_roles(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return (role.__dict__ for role in current_user.roles)
