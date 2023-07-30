from sqlalchemy.orm import Session

from auth.helper.password_helper import PasswordHelper
from auth.models.user_model import UserModel
from auth.schemas.user_schema import UserInSchema, UserSchema
from core.error import ErrorCode, FastAPIException


class UserHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        return self.session.query(UserModel).offset(skip).limit(limit).all()

    def get_user(self, user_id: int | None = None, email: str | None = None) -> UserModel | None:
        if user_id is not None:
            return self.session.query(UserModel).filter(UserModel.id == user_id).first()

        if email is not None:
            return self.session.query(UserModel).filter(UserModel.email == email).first()

    def create_user(self, user_in: UserInSchema) -> UserModel:
        if self.get_user(email=user_in.email) is not None:
            raise FastAPIException(ErrorCode.AUTH_4091)

        hashed_password = PasswordHelper.render(user_in.password)
        user = UserSchema(**user_in.model_dump(exclude_none=True), hashed_password=hashed_password)
        db_user = UserModel(**user.model_dump(exclude_none=True))

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def get_or_create_user(self, user_in: UserInSchema) -> UserModel:
        user_db = self.get_user(email=user_in.email)
        return user_db if user_db is not None else self.create_user(user_in=user_in)

    def delete_user(self, user_db: UserModel | None = None, user_id: int | None = None):
        if user_db is None:
            user_db = self.get_user(user_id=user_id)

        self.session.delete(user_db)
        self.session.commit()
