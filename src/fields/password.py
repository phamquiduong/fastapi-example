import re
from typing import Annotated

from pydantic import Field
from pydantic.functional_validators import AfterValidator
from pydantic_core import PydanticCustomError

from errors.type import ErrorType

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,64}$"


def validate_password(v: str) -> str:
    if not re.fullmatch(PASSWORD_REGEX, v):
        raise PydanticCustomError(
            ErrorType.NOT_MATCH_REGEX.value, "Password does not match the regex.", {"regex": PASSWORD_REGEX}
        )
    return v


PasswordField = Annotated[
    str,
    Field(
        title="Password",
        description="Strong password (8-64 chars, include uppercase, lowercase, number and special character).",
        min_length=8,
        max_length=64,
        examples=["P@ssw0rd123!"],
        json_schema_extra={
            "format": "password",
            "writeOnly": True,
        },
        exclude=True,
    ),
    AfterValidator(validate_password),
]
