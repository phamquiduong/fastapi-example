from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.crud.role_crud import get_role
from auth.crud.user_crud import get_user
from auth.models.user_role_model import UserModel
from core.dependencies.db_depend import get_session
from core.helper.token_helper import access_token_helper

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    try:
        user_id: str = access_token_helper.auth_token(token)
        return get_user(session=session, user_id=user_id)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))


async def get_current_active_user(current_user: Annotated[UserModel, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: Annotated[UserModel, Depends(get_current_active_user)], session: Session = Depends(get_session)):
    admin_role = get_role(session, 'admin')
    if admin_role not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have admin role")
    return current_user
