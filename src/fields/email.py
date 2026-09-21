from typing import Annotated

from pydantic import EmailStr, Field

EmailField = Annotated[EmailStr, Field(max_length=255)]
