from core.helper.bcrypt_helper import bcrypt_helper
from core.settings import settings


class PasswordHelper:
    def __init__(self, password_salt: str) -> None:
        self.password_salt = password_salt

    def verify(self, password: str, hasher_password: str):
        password += self.password_salt

        return bcrypt_helper.verify(plain_text=password, hashed_text=hasher_password)

    def render(self, password: str):
        password += self.password_salt

        return bcrypt_helper.hash(password)


password_helper = PasswordHelper(password_salt=settings.password_salt)
