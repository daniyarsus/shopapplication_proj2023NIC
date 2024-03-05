from abc import ABC, abstractmethod

from typing import Dict, Any, List

from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.auth.models import User
from api.internal.management.crud.employee import schemas
from api.internal.management.models import Employee


class BaseEmployeeManager(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create_employee(self, create_data: schemas.CreateEmployee) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update_employee(self, update_data: schemas.UpdateEmployee) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def delete_employee(self, delete_data: schemas.DeleteEmployee) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_all_employee(self) -> List[Dict[str, Any]]:
        pass


class EmployeeManager(BaseEmployeeManager):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create_employee(self, create_data: schemas.CreateEmployee) -> Dict[str, Any]:
        try:
            query = select(User).where(User.id == create_data.id)
            result = await self.db.execute(query)
            employee = result.scalar_one_or_none()

            if employee:
                employee.permission = create_data.permission

                await self.db.commit()
                await self.db.refresh(employee)

            worker = Employee(
                user_id=create_data.id,
                username=employee.username,
                permission=create_data.permission
            )

            self.db.add(worker)
            await self.db.commit()

            return {"message": "Employee created successfully", "id": employee.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_employee(self, update_data: schemas.UpdateEmployee) -> Dict[str, Any]:
        try:
            query = select(Employee).where(Employee.id == update_data.id)
            result = await self.db.execute(query)
            employee = result.scalar_one_or_none()

            if employee:
                employee.permission = update_data.permission
                employee.changed_on = datetime.utcnow()

                await self.db.commit()
                await self.db.refresh(employee)

                return {"message": "Employee updated successfully", "employee_id": employee.id}

            else:
                raise HTTPException(status_code=404, detail="Employee not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_employee(self, delete_data: schemas.DeleteEmployee) -> Dict[str, Any]:
        try:
            query = select(Employee).where(Employee.id == delete_data.id)
            result = await self.db.execute(query)
            employee = result.scalar_one_or_none()

            if employee:
                await self.db.delete(employee)
                await self.db.commit()

                return {"message": "Employee deleted successfully", "employee_id": employee.id}

            else:
                raise HTTPException(status_code=404, detail="Employee not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_employee(self) -> List[Dict[str, Any]]:
        query = select(Employee)
        result = await self.db.execute(query)
        employee = result.scalars().all()
        employee_data = [
            {"id": employee.id,
             "user_id": employee.user_id,
             "username": employee.username,
             "permission": employee.permission}
            for employee in employee
        ]

        return employee_data
