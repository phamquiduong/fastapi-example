from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.helper.database_helper import db_helper

Base = db_helper.get_base()


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

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
