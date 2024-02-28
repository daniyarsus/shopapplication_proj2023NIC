from typing import Annotated

from pydantic import (BaseModel,
                      Field)


class Employee(BaseModel):
    id: Annotated[int, Field(...)]


class CreateEmployee(Employee):
    permission: Annotated[int, Field(...)]


class UpdateEmployee(Employee):
    permission: Annotated[int, Field(...)]


class DeleteEmployee(Employee):
    pass

