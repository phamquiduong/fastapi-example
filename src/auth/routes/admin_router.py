from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.orm import Session

from auth.crud.user_crud import (delete_user, get_user, get_users, update_user,
                                 update_user_add_role, update_user_remove_role)
from auth.dependencies.auth_depend import get_current_admin_user
from auth.models.user_role_model import UserModel
from auth.schemas.role_schema import RoleEnum, RoleOutSchema
from auth.schemas.user_schema import (UserOutSchema, UserRoleOutSchema,
                                      UserUpdateSchema)
from core.dependencies.db_depend import get_session
from core.schemas.error_schema import (HTTPExceptionSchema,
                                       RequestValidationErrorSchema)

admin_route = APIRouter(prefix='/users', tags=['Adminstrator'])


@admin_route.get('', response_model=list[UserRoleOutSchema],
                 responses={
    401: {'model': HTTPExceptionSchema},
    403: {'model': HTTPExceptionSchema},
    404: {'model': HTTPExceptionSchema},
    422: {'model': RequestValidationErrorSchema},
    500: {'model': HTTPExceptionSchema},
})
def admin_get_users(
    admin_user: UserModel = Depends(get_current_admin_user),
    ignore_admin: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    session: Session = Depends(get_session),
):
    return ({
        'user': user.__dict__,
        'roles': (role.__dict__ for role in user.roles)
    } for user in get_users(session=session, limit=limit, skip=skip, ignore_admin=ignore_admin))


@admin_route.get('/{user_id}', response_model=UserRoleOutSchema,
                 responses={
                     401: {'model': HTTPExceptionSchema},
                     403: {'model': HTTPExceptionSchema},
                     404: {'model': HTTPExceptionSchema},
                     422: {'model': RequestValidationErrorSchema},
                     500: {'model': HTTPExceptionSchema},
                 })
def admin_get_user(
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    session: Session = Depends(get_session),
):
    user = get_user(session=session, user_id=user_id)
    return {
        'user': user.__dict__,
        'roles': (role.__dict__ for role in user.roles)
    }


@admin_route.put('/{user_id}', response_model=UserOutSchema,
                 responses={
                     401: {'model': HTTPExceptionSchema},
                     403: {'model': HTTPExceptionSchema},
                     404: {'model': HTTPExceptionSchema},
                     422: {'model': RequestValidationErrorSchema},
                     500: {'model': HTTPExceptionSchema},
                 })
def admin_update_user(
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    user_update: Annotated[UserUpdateSchema, Body(...)],
    session: Session = Depends(get_session),
):
    return update_user(session=session, user_id=user_id, user=user_update).__dict__


@admin_route.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT,
                    responses={
                        401: {'model': HTTPExceptionSchema},
                        403: {'model': HTTPExceptionSchema},
                        404: {'model': HTTPExceptionSchema},
                        422: {'model': RequestValidationErrorSchema},
                        500: {'model': HTTPExceptionSchema},
                    })
def admin_delete_user(
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    session: Session = Depends(get_session),
):
    delete_user(session=session, user_id=user_id)


@admin_route.post('/{user_id}/role', response_model=list[RoleOutSchema],
                  responses={
    401: {'model': HTTPExceptionSchema},
    403: {'model': HTTPExceptionSchema},
    404: {'model': HTTPExceptionSchema},
    422: {'model': RequestValidationErrorSchema},
    500: {'model': HTTPExceptionSchema}
})
def admin_add_user_role(
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    role_name: Annotated[RoleEnum, Body(...)],
    session: Session = Depends(get_session),
):
    user_db = update_user_add_role(session=session, role_name=role_name, user_id=user_id)
    return (role.__dict__ for role in user_db.roles)


@admin_route.delete('/{user_id}/role', response_model=list[RoleOutSchema],
                    responses={
    401: {'model': HTTPExceptionSchema},
    403: {'model': HTTPExceptionSchema},
    404: {'model': HTTPExceptionSchema},
    422: {'model': RequestValidationErrorSchema},
    500: {'model': HTTPExceptionSchema}
})
def admin_remove_user_role(
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    role_name: Annotated[RoleEnum, Body(...)],
    session: Session = Depends(get_session),
):
    user_db = update_user_remove_role(session=session, role_name=role_name, user_id=user_id)
    return (role.__dict__ for role in user_db.roles)
