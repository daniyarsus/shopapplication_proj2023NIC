from typing import Annotated

from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      ConfigDict,
                      validator)


class PasswordEmailSendSchema(BaseModel):
    email: EmailStr


class PasswordPasswordVerifySchema(BaseModel):
    email: EmailStr
    new_password: Annotated[str, Field(min_length=1, max_length=24)]
    code: Annotated[str, Field(min_length=6, max_length=6)]
