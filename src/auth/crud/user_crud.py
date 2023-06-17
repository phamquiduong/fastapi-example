from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import not_

from auth.crud.role_crud import get_role
from auth.helper.password_helper import password_helper
from auth.models.user_role_model import RoleModel, UserModel
from auth.schemas.user_schema import UserInSchema, UserSchema, UserUpdateSchema


def get_users(session: Session, skip: int = 0, limit: int = 100, ignore_admin: bool = False) -> list[UserModel]:
    users = session.query(UserModel)
    users = users.filter(not_(UserModel.roles.contains(get_role(session, 'admin')))) if ignore_admin else users
    return users.offset(skip).limit(limit).all()


def get_user(session: Session, user_id: int = None, email: str = None, check_exist: bool = True):
    if user_id is not None:
        user = session.query(UserModel).filter(UserModel.id == user_id).first()

    if email is not None:
        user = session.query(UserModel).filter(UserModel.email == email).first()

    if check_exist and user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


def create_user(session: Session, user: UserInSchema):
    if get_user(session=session, email=user.email, check_exist=False) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exist')

    hashed_password = password_helper.render(user.password)
    user_schema = UserSchema(**user.__dict__, hashed_password=hashed_password)
    db_user = UserModel(**user_schema.__dict__)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_or_create_user(session: Session, user: UserInSchema) -> UserModel:
    user_db = get_user(session=session, email=user.email, check_exist=False)

    if user_db is not None:
        return user_db

    return create_user(session=session, user=user)


def update_user(session: Session, user: UserUpdateSchema, user_db: UserModel | None = None, user_id: int | None = None):
    if user_db is None:
        user_db = get_user(session=session, user_id=user_id)

    for key, value in user.__dict__.items():
        if value is not None:
            setattr(user_db, key, value)

    session.commit()
    session.refresh(user_db)

    return user_db


def update_user_add_role(session: Session, role_db: RoleModel | None = None, role_name: str | None = None,
                         user_db: UserModel | None = None, user_id: int | None = None):
    if user_db is None:
        user_db = get_user(session=session, user_id=user_id)

    if role_db is None:
        role_db = get_role(session=session, role_name=role_name)

    if role_db not in user_db.roles:
        user_db.roles.append(role_db)

    session.commit()
    session.refresh(user_db)

    return user_db


def update_user_remove_role(session: Session, role_db: RoleModel | None = None, role_name: str | None = None,
                            user_db: UserModel | None = None, user_id: int | None = None):
    if user_db is None:
        user_db = get_user(session=session, user_id=user_id)

    if role_db is None:
        role_db = get_role(session=session, role_name=role_name)

    if role_db in user_db.roles:
        user_db.roles.remove(role_db)

    session.commit()
    session.refresh(user_db)

    return user_db


def delete_user(session: Session, user_db: UserModel | None = None, user_id: int | None = None):
    if user_db is None:
        user_db = get_user(session=session, user_id=user_id)

    session.delete(user_db)
    session.commit()
