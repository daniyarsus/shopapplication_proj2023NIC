from typing import Annotated

from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      ConfigDict,
                      validator)


class SignupSchema(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    lastname: Annotated[str, Field(min_length=1, max_length=255)]
    email: EmailStr
    phone: Annotated[str, Field(...)]
    username: Annotated[str, Field(min_length=1, max_length=24)]
    password: Annotated[str, Field(min_length=1, max_length=24)]

    class Config:
        from_attributes = True


class SignupEmailSend(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class SignupEmailVerify(BaseModel):
    email: EmailStr
    verification_code: Annotated[int, Field(min_length=6, max_length=6)]

    class Config:
        from_attributes = True
