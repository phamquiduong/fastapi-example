from pydantic import BaseModel, ConfigDict, EmailStr, validator

from core.validator.phone_number_validator import phone_number_validator


class UserBaseSchema(BaseModel):
    email: EmailStr

    # Optional fields
    address: str | None = None
    full_name: str | None = None
    phone_number: str | None = None

    @validator('phone_number')
    @classmethod
    def user_phone_number_validator(cls, phone_number):
        return phone_number_validator(phone_number) if phone_number else None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "address": "Da Nang, Viet Nam",
            "full_name": "FastAPI New User",
            "phone_number": "+84 123 456 789"}})


class UserSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: str


class UserInSchema(UserBaseSchema):
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "FastAPIStrongPassword!@#123",
            "address": "Da Nang, Viet Nam",
            "full_name": "FastAPI New User",
            "phone_number": "+84 123 456 789"}})


class UserOutSchema(UserBaseSchema):
    id: int
    is_active: bool

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "is_active": True,
            "email": "user@example.com",
            "address": "Da Nang, Viet Nam",
            "full_name": "FastAPI New User",
            "phone_number": "+84 123 456 789"}})


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "FastAPIStrongPassword!@#123"}})
