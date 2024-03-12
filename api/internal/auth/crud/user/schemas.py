from typing import Annotated

from pydantic import (BaseModel,
                      Field,
                      EmailStr)


class User(BaseModel):
    name: Annotated[str, Field(...)]
    lastname: Annotated[str, Field(...)]
    email: EmailStr
    phone: Annotated[str, Field(...)]
    username: Annotated[str, Field(...)]
    password: Annotated[str, Field(...)]
    is_active: Annotated[bool, Field(...)]
    is_verified: Annotated[bool, Field(...)]
    permission: Annotated[int, Field(...)]

    class Config:
        from_attributes = True


class CreateUser(User):
    pass


class UpdateUser(BaseModel):
    id: Annotated[int, Field(...)]


class DeleteUser(BaseModel):
    id: Annotated[int, Field(...)]
