from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.helper.database_helper import database_helper

Base = database_helper.get_base()

UserRole = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
)


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)

    # Optional fields
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)

    roles: Mapped[List[RoleModel]] = relationship(secondary=UserRole, back_populates="users")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, UserModel):
            return False
        return self.id == obj.id


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    users: Mapped[List[UserModel]] = relationship(secondary=UserRole, back_populates="roles")

    def __repr__(self) -> str:
        return f"<Role(name={self.name})>"

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, RoleModel):
            return False
        return self.id == obj.id
