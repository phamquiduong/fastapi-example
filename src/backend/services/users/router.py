from typing import Annotated, List

from fastapi import (APIRouter, Body, Depends, HTTPException, Path, Query,
                     status)
from sqlalchemy.orm import Session

from auth.dependencies import get_current_active_user, get_current_admin_user
from core.constants import DEFAULT_ROLE, ROLES
from core.dependencies import get_db
from users import models as user_models
from users import schemas as user_schemas
from users.crud import (create_user, delete_user, get_user, get_users,
                        update_user)

user_route = APIRouter(prefix='/user', tags=['User'])
admin_user_route = APIRouter(prefix='/users', tags=['Admin'])


############################
# User functions
############################
@user_route.get('', response_model=user_schemas.User)
def get_current_user(
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
):
    return current_user.__dict__


@user_route.put('', status_code=status.HTTP_204_NO_CONTENT)
def update_current_user(
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    user: Annotated[user_schemas.UserUpdate, Body(...)],
    db: Session = Depends(get_db),
):
    update_user(db, db_user=current_user, user=user)


@user_route.delete('', status_code=status.HTTP_204_NO_CONTENT)
def remove_current_user(
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    delete_user(db=db, user=current_user)


@user_route.get('/role')
def get_current_user_roles(
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return user_schemas.UserRole(
        user=user_schemas.User(**current_user.__dict__),
        roles=current_user.roles
    )


############################
# Admin functions
############################
@admin_user_route.get('', response_model=list[user_schemas.User])
async def admin_get_users(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    skip: Annotated[int, Query(..., ge=0)] = 0,
    limit: Annotated[int, Query(..., gt=0, le=100)] = 10,
    db: Session = Depends(get_db),
):
    return (user.__dict__ for user in get_users(db, limit=limit, skip=skip))


@admin_user_route.post('', response_model=user_schemas.User)
async def admin_create_user(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_create: Annotated[user_schemas.UserCreate, Body(...)],
    db: Session = Depends(get_db),
):
    if get_user(db, email=user_create.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already registered')
    return create_user(db, user_create, DEFAULT_ROLE).__dict__


@admin_user_route.get('/{user_id}', response_model=user_schemas.User)
def admin_get_user(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.__dict__


@admin_user_route.put('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def admin_update_user(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    user: Annotated[user_schemas.UserUpdate, Body(...)],
    db: Session = Depends(get_db),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_user(db, db_user=db_user, user=user)


@admin_user_route.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    delete_user(db, user)


@admin_user_route.get('/{user_id}/role')
def admin_get_user_role(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    db: Session = Depends(get_db),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_schemas.UserRole(
        user=user_schemas.User(**db_user.__dict__),
        roles=db_user.roles
    )


@admin_user_route.post('/{user_id}/role', status_code=status.HTTP_204_NO_CONTENT)
def admin_add_user_role(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    role_name: Annotated[str, Body(...)],
    db: Session = Depends(get_db),
):
    if role_name not in ROLES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Role name is invalid')

    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_user(db, db_user=db_user, role_name=role_name, role_action='add')


@admin_user_route.delete('/{user_id}/role', status_code=status.HTTP_204_NO_CONTENT)
def admin_remove_user_role(
    admin_user: Annotated[user_models.User, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(..., gt=0)],
    role_name: Annotated[str, Body(...)],
    db: Session = Depends(get_db),
):
    if role_name not in ROLES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Role name is invalid')

    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_user(db, db_user=db_user, role_name=role_name, role_action='remove')
