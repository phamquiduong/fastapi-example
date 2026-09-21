from uuid import UUID, uuid7

from sqlmodel import Field, SQLModel


class UUIDMixin(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid7)
