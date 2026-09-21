from pydantic import EmailStr
from sqlmodel import Field

from models.base import UUIDMixin


class User(UUIDMixin, table=True):
    __tablename__: str = "users"

    email: EmailStr = Field(max_length=255, unique=True)
    password: str = Field(max_length=255)
