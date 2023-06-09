from sqlalchemy.orm import Session

from auth.helper.hasher_helper import Hasher
from core.constants import PASSWORD_SALT, ROLE_ACTIONS
from users import models, schemas


################################
# User CRUD methods
################################
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int = None, email: str = None):
    if user_id is not None:
        return db.query(models.User).filter(models.User.id == user_id).first()

    if email is not None:
        return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, role_name: str = None):
    password_with_salt = user.password + PASSWORD_SALT
    hashed_password = Hasher.get_password_hash(password_with_salt)
    role = get_role(db, role_name=role_name)

    db_user = models.User(**schemas.UserBase(**user.__dict__).__dict__, hashed_password=hashed_password)
    db_user.roles.append(role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, db_user: models.User, user: schemas.UserUpdate = None,
                role_name: str = None, role_action: str = None):
    if user is not None:
        for key, value in user.__dict__.items():
            setattr(db_user, key, value)

    if role_name is not None and role_action in ROLE_ACTIONS:
        role = get_role(db, role_name=role_name)

        if role_action == 'add' and role not in db_user.roles:
            db_user.roles.append(role)

        if role_action == 'remove' and role in db_user.roles:
            db_user.roles.remove(role)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()


################################
# Role CRUD methods
################################
def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()


def get_role(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.name == role_name).first()


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.__dict__)

    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role


def get_or_create_role(db: Session, role_name: str) -> models.Role:
    role = get_role(db, role_name)
    if role is None:
        role_create = schemas.RoleCreate(name=role_name)
        role = create_role(db, role_create)
    return role
