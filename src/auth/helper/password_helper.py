from core.helper.bcrypt_helper import BcryptHelper
from core.settings import settings


class PasswordHelper:
    @staticmethod
    def verify(password: str, hasher_password: str):
        password += settings.password_salt
        return BcryptHelper().verify(plain_text=password, hashed_text=hasher_password)

    @staticmethod
    def render(password: str):
        password += settings.password_salt
        return BcryptHelper().hash(password)
