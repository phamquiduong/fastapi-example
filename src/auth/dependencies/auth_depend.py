from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.helper.auth_helper import AuthHelper
from auth.helper.token_helper import AccessTokenHelper
from core.dependencies.db_depend import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    return AuthHelper(session).by_token(token=token, helper=AccessTokenHelper())
