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
    phone: str
    username: Annotated[str, Field(min_length=1, max_length=24)]
    password: Annotated[str, Field(min_length=1, max_length=24)]

    #model_config = ConfigDict(from_attributes=True)

    #@validator("phone")
    #def validate_phone(cls, v):
    #    if (v[number] == "+" and v[number+1] == "7") or (v[number] == "8" and v[number+1] == "7"):
    #        pass
    #    else:
    #        raise ValueError("Некорректный номер!")


class SignupEmailSend(BaseModel):
    email: EmailStr


class SignupEmailVerify(BaseModel):
    email: EmailStr
    verification_code: Annotated[int, Field(min_length=6, max_length=6)]
