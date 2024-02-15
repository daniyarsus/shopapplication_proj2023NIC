from fastapi import HTTPException

from src.database.models import Employee


class EmployeeManager:
    def __init__(self, current_user, db):
        self.current_user = current_user
        self.db = db

    async def _check_owner(self):
        owner = self.db.query(Employee).filter(
            Employee.user_id == self.current_user.id,
            Employee.position == "owner"
        ).first()
        if not owner:
            raise HTTPException(status_code=403, detail="You must be an owner to perform this operation")

    async def _check_employee(self):
        employee_to_delete = self.db.query(Employee).filter(Employee.user_id == delete_data.user_id).first()
        if not employee_to_delete:
            raise HTTPException(status_code=404, detail="Employee not found")

    async def add_employee(self, create_data):
        await self._check_owner()

        return {"message": "Employee added successfully",
                "employee_id": create_data.user_id}

    async def update_employee_position(self, update_data):
        await self._check_owner()

        await self._check_employee()

        employee_to_update.position = update_data.position
        self.db.commit()

        return {"message": "Employee's position updated successfully",
                "user_id": update_data.user_id,
                "new_position": update_data.position}

    async def delete_employee(self, delete_data):
        await self._check_owner()

        await self._check_employee()

        self.db.delete(employee_to_delete)
        self.db.commit()

        return {"message": "Employee deleted successfully",
                "employee_id": delete_data.user_id}

    async def get_employee_position(self):
        await self._check_owner()

        try:
            employee = self.db.query(Employee).all()
            return employee
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

