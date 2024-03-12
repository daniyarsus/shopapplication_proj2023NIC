from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.services.auth.models import User
from api.internal.management.crud.employee.controllers import EmployeeManager
from api.internal.management.crud.employee import schemas

management_router = APIRouter()


@management_router.post("/create-employee")
async def create_employee_endpoint(create_data: schemas.CreateEmployee = Depends(),
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    employee_manager = EmployeeManager(current_user=current_user,
                                       db=db)
    result = await employee_manager.create_employee(create_data=create_data)
    return result


@management_router.put("/update-employee")
async def update_employee_endpoint(update_data: schemas.UpdateEmployee = Depends(),
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    employee_manager = EmployeeManager(current_user=current_user,
                                       db=db)
    result = await employee_manager.update_employee(update_data=update_data)
    return result


@management_router.delete("/delete-employee")
async def delete_employee_endpoint(delete_data: schemas.DeleteEmployee = Depends(),
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    employee_manager = EmployeeManager(current_user=current_user,
                                       db=db)
    result = await employee_manager.delete_employee(delete_data=delete_data)
    return result


@management_router.get("/get-all-employee")
async def get_employee_endpoint(db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user)
                                ):
    employee_manager = EmployeeManager(current_user=current_user,
                                       db=db)
    result = await employee_manager.get_all_employee()
    return result
