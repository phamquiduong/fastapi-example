from fastapi import APIRouter, HTTPException, status

from dependencies.services.user import UserServiceDep
from schemas.user.public import UserPublic
from schemas.user.register import UserRegister

users_router = APIRouter(prefix="/users", tags=["User"])


@users_router.post("")
async def register_user(user_register: UserRegister, user_service: UserServiceDep) -> UserPublic:
    if await user_service.get_by_email(email=user_register.email) is not None:
        raise HTTPException(detail="User already exist", status_code=status.HTTP_409_CONFLICT)

    user = await user_service.create(user_register)
    return UserPublic.model_validate(user.model_dump())
