from enum import Enum

from pydantic import BaseModel


class RoleBaseSchema(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "admin"
            },
        }


class RoleInSchema(RoleBaseSchema):
    pass


class RoleOutSchema(RoleBaseSchema):
    id: int


class RoleSchema(RoleBaseSchema):
    id: int

    class Config:
        orm_mode = True


class RoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'
