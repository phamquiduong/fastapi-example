from sqlalchemy.orm import Session

from auth.helper.password_helper import PasswordHelper
from auth.helper.token_helper import AccessTokenHelper, RefreshTokenHelper
from auth.helper.user_helper import UserHelper
from auth.models.user_model import UserModel
from core.error import ErrorCode, FastAPIException


class AuthHelper:
    def __init__(self, session: Session):
        self.session = session

    def by_email_password(self, email: str, password: str) -> UserModel:
        user = UserHelper(session=self.session).get_user(email=email)

        user = self.__check_found(user)
        self.__check_password(user=user, password=password)
        self.__check_active(user)

        return user

    def by_token(self, token: str, helper: AccessTokenHelper | RefreshTokenHelper) -> UserModel:
        user_id: int = helper.auth_token(token)
        user = UserHelper(self.session).get_user(user_id=user_id)

        user = self.__check_found(user)
        self.__check_active(user)

        return user

    def __check_found(self, user: UserModel | None) -> UserModel:
        if user is None:
            raise FastAPIException(ErrorCode.AUTH_4012)
        return user

    def __check_password(self, user: UserModel, password: str):
        if not PasswordHelper.verify(password, user.hashed_password):
            raise FastAPIException(ErrorCode.AUTH_4013)

    def __check_active(self, user: UserModel):
        if not user.is_active:
            raise FastAPIException(ErrorCode.AUTH_4014)
