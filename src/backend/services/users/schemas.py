from typing import List

from pydantic import BaseModel, EmailStr


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr

    # Optional fields
    address: str | None
    full_name: str | None
    phone_number: str | None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr | None
    is_active: bool | None


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserRole(BaseModel):
    user: User
    roles: List[Role]
