from fastapi import APIRouter, status

from dependencies.services.user import UserServiceDep
from errors.api_exception import APIException
from errors.type import ErrorType
from schemas.error import ErrorResponse, FieldError
from schemas.user.public import UserPublic
from schemas.user.register import UserRegister

users_router = APIRouter(prefix="/users", tags=["User"])


@users_router.post("", responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponse}})
async def register_user(user_register: UserRegister, user_service: UserServiceDep) -> UserPublic:
    if await user_service.get_by_email(email=user_register.email) is not None:
        raise APIException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with the email already registered.",
            fields=FieldError(
                name="email", message="Email already exists.", type=ErrorType.CONFLICT, input=user_register.email
            ),
        )

    user = await user_service.create(user_register)
    return UserPublic.model_validate(user.model_dump())
