from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, DeclarativeBase

from database import Base


class MyDeclarativeBase(DeclarativeBase):
    pass


UserRole = Table(
    'users_roles',
    MyDeclarativeBase.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    roles = relationship('Role', secondary=UserRole, backref='users')


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, index=True)

    users = relationship('User', secondary=UserRole, backref='users')
