from typing import Annotated

from pydantic import (BaseModel,
                      Field)


class Employee(BaseModel):
    id: Annotated[int, Field(...)]

    class Config:
        from_attributes = True


class CreateEmployee(Employee):
    permission: Annotated[int, Field(...)]


class UpdateEmployee(Employee):
    permission: Annotated[int, Field(...)]


class DeleteEmployee(Employee):
    pass


#class EmployeeSchema:
#    def __init__(self):
#        self.create = CreateEmployee()
#        self.update = UpdateEmployee()
#        self.delete = DeleteEmployee()
#
#
#employee_schema: EmployeeSchema = EmployeeSchema()
