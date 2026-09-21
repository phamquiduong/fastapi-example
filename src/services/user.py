from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User
from schemas.user.register import UserRegister
from utils.password import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_register: UserRegister) -> User:
        password_hashed = get_password_hash(user_register.password)
        user = User(email=user_register.email, password=password_hashed)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        result = await self.session.exec(select(User).where(User.email == email))
        return result.first()
