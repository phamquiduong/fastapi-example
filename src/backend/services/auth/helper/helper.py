from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.helper.hasher_helper import Hasher
from core.constants import PASSWORD_SALT
from users import models
from users.crud import get_user


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    """Authenticate a user using the given email and password

    Args:
        db (Session): DB Session
        email (str): email to authenticate
        password (str): password to authenticate

    Raises:
        HTTPException: User is not found when email are not existing
        HTTPException: Password is incorrect when password is incorrect

    Returns:
        models.User: User model instance
    """

    user = get_user(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not found')
    if not Hasher.verify_password(password+PASSWORD_SALT, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password is incorrect')
    return user
