from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
