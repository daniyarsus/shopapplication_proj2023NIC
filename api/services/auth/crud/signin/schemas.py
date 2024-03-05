from typing import Annotated
from pydantic import (BaseModel,
                      Field)


class SigninSchema(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=25)]
    password: Annotated[str, Field(min_length=3, max_length=25)]
