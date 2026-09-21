from pydantic import BaseModel

from fields.email import EmailField
from fields.password import PasswordField


class UserRegister(BaseModel):
    email: EmailField
    password: PasswordField
