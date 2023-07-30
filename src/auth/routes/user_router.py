from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies.auth_depend import get_current_user
from auth.helper.user_helper import UserHelper
from auth.models.user_model import UserModel
from auth.schemas.user_schema import UserOutSchema
from core.dependencies.db_depend import get_session

user_route = APIRouter(prefix='/user', tags=['User'])


@user_route.get('', response_model=UserOutSchema)
def get_user(
    current_user: UserModel = Depends(get_current_user),
):
    return current_user.__dict__


@user_route.delete('', status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    UserHelper(session).delete_user(user_db=current_user)
