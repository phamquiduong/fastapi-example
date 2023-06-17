from pydantic import BaseModel, EmailStr, validator

from auth.schemas.role_schema import RoleOutSchema
from core.helper.phone_number_helper import PhoneNumberHelper


class UserBaseSchema(BaseModel):
    email: EmailStr

    # Optional fields
    address: str | None
    full_name: str | None
    phone_number: str | None

    @validator('phone_number')
    def phone_number_validator(cls, phone_number):
        return PhoneNumberHelper(phone_number).validator() if phone_number is not None else None

    class Config:
        schema_extra = {
            "example": {
                "email": "fast_api_base@mail.com",
                "address": "Da Nang, Viet Nam",
                "full_name": "Fast API Base Source",
                "phone_number": "+84 123 456 789"
            },
        }


class UserInSchema(UserBaseSchema):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fast_api_base@mail.com",
                "password": "Hello123!@#",
                "address": "Da Nang, Viet Nam",
                "full_name": "Fast API Base Source",
                "phone_number": "+84 123 456 789"
            },
        }


class UserOutSchema(UserBaseSchema):
    id: int
    is_active: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "fast_api_base@mail.com",
                "is_active": True,
                "address": "Da Nang, Viet Nam",
                "full_name": "Fast API Base Source",
                "phone_number": "+84 123 456 789",
            },
        }


class UserUpdateSchema(UserBaseSchema):
    email: EmailStr | None
    is_active: bool | None

    class Config:
        schema_extra = {
            "example": {
                "email": "fast_api_base@mail.com",
                "is_active": True,
                "address": "Da Nang, Viet Nam",
                "full_name": "Fast API Base Source",
                "phone_number": "+84 123 456 789",
            },
        }


class UserSchema(UserBaseSchema):
    id: int | None
    is_active: bool = True
    hashed_password: str

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fast_api_base@mail.com",
                "password": "Hello123!@#"
            },
        }


class UserRoleOutSchema(BaseModel):
    user: UserOutSchema
    roles: list[RoleOutSchema]
