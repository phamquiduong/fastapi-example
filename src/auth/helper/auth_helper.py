from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.crud.user_crud import get_user
from auth.helper.password_helper import password_helper


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email=email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not found')

    if not password_helper.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password is incorrect')

    return user
