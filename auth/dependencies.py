from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.helper.token_helper import AccessTokenHelper
from core.dependencies import get_db
from core.helper.jwt_helper import jwt_helper
from users import models as user_models
from users.crud import get_role, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    access_token_helper = AccessTokenHelper()
    try:
        user_id: str = access_token_helper.auth_token(token)
        return get_user(db=db, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def get_current_active_user(current_user: Annotated[user_models.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: Annotated[user_models.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    admin_role = get_role(db, 'admin')
    if admin_role not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have admin role")
    return current_user
