from typing import Annotated

from fastapi import Depends

from dependencies.database import SessionDep
from services.user import UserService


async def get_user_service(session: SessionDep):
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
