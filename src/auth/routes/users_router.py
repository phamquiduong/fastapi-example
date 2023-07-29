from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from auth.helper.user_helper import UserHelper
from auth.schemas.user_schema import UserOutSchema
from core.dependencies.db_depend import get_session
from core.error import ErrorCode, FastAPIException
from core.settings import settings

users_route = APIRouter(prefix='/users', tags=['Users'])


@users_route.get('', response_model=list[UserOutSchema])
def get_all_users(
    page: int | None = Query(None),
    skip: int = Query(0, gt=-1),
    limit: int = Query(settings.limit, gt=0, lt=settings.limit+1),
    session: Session = Depends(get_session)
):
    if page is not None:
        skip = page*settings.limit
    return UserHelper(session).get_users(skip=skip, limit=limit)


@users_route.get('/{user_id}', response_model=UserOutSchema)
def get_user(
    user_id: int = Path(..., gt=0),
    session: Session = Depends(get_session)
):
    user = UserHelper(session).get_user(user_id=user_id)
    if user is None:
        raise FastAPIException(ErrorCode.AUTH_4012)
    return user.__dict__
