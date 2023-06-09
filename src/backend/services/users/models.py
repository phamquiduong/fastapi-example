from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.config import Base

UserRole = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)

    # Optional fields
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)

    roles: Mapped[List[Role]] = relationship(secondary=UserRole, back_populates="users")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    def __eq__(self, obj):
        if not isinstance(obj, User):
            return False
        return self.id == obj.id


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    users: Mapped[List[User]] = relationship(secondary=UserRole, back_populates="roles")

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"

    def __eq__(self, obj):
        if not isinstance(obj, Role):
            return False
        return self.id == obj.id
