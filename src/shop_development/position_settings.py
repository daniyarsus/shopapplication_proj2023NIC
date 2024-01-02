from fastapi import Depends, HTTPException

from src.database.models import User, Employee
from src.settings.config import SessionLocal


async def add_employee(new_employee, current_user):
    session = SessionLocal()

    try:
        # Проверяем, является ли текущий пользователь владельцем
        owner = session.query(Employee).filter(Employee.user_id == current_user.id,
                                               Employee.position == "owner").first()
        if not owner:
            raise HTTPException(status_code=403, detail="You must be an owner to add employees")

        # Создаем новую запись сотрудника
        employee = Employee(
            user_id=new_employee.user_id
        )
        session.add(employee)
        session.commit()

        return {"message": "Employee added successfully", "employee_id": new_employee.user_id}

    except Exception as e:
        print(f"Error adding employee: {e}")
        raise HTTPException(status_code=500, detail="Error adding employee")

    finally:
        session.close()


async def delete_employee(employee_data, current_user):
    session = SessionLocal()

    try:
        owner = session.query(Employee).filter(Employee.user_id == current_user.id,
                                               Employee.position == "owner").first()
        if not owner:
            raise HTTPException(status_code=403, detail="You must be an owner to delete employees")

        # Находим и удаляем сотрудника
        employee_to_delete = session.query(Employee).filter(Employee.user_id == employee_data.user_id).first()
        if not employee_to_delete:
            raise HTTPException(status_code=404, detail="Employee not found")

        session.delete(employee_to_delete)
        session.commit()

        return {"message": "Employee deleted successfully", "employee_id": employee_data.employee_id}

    except Exception as e:
        print(f"Error deleting employee: {e}")
        raise HTTPException(status_code=500, detail="Error deleting employee")

    finally:
        session.close()


async def update_position_employee(position_data, current_user):
    session = SessionLocal()
    try:
        # Получаем сессию и проверяем, является ли текущий пользователь владельцем
        owner = session.query(Employee).filter(Employee.user_id == current_user.id,
                                               Employee.position == "owner").first()
        if not owner:
            raise HTTPException(status_code=403, detail="You must be an owner to update employee positions")

        # Находим сотрудника, чью должность нужно обновить
        employee_to_update = session.query(Employee).filter(Employee.user_id == position_data.user_id).first()
        if not employee_to_update:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Обновляем должность сотрудника
        employee_to_update.position = position_data.position
        session.commit()

        return {"message": "Employee's position updated successfully", "employee_id": position_data.user_id,
                "new_position": position_data.position}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Error updating employee's position: {e}")
        raise HTTPException(status_code=500, detail="Error updating employee's position")

    finally:
        session.close()

