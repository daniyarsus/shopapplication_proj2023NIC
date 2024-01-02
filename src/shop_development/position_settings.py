from fastapi import Depends

from src.database.models import User, Employee
from src.settings.config import SessionLocal


async def add_employee(new_employee, current_user):
    session = SessionLocal()

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


async def delete_employee(employee_data, current_user):
    session = SessionLocal()

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


async def update_employee_position(update_data, current_user: User):
    session = SessionLocal()

    try:
        # Проверка, является ли текущий пользователь владельцем
        owner = session.query(Employee).filter(Employee.user_id == current_user.id, Employee.position == "owner").first()
        if not owner:
            raise HTTPException(status_code=403, detail="You must be an owner to update positions")

        # Находим сотрудника для обновления
        employee = session.query(Employee).filter(Employee.user_id == update_data.user_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Обновляем позицию сотрудника
        employee.position = update_data.position
        session.commit()

        return {"message": "Employee's position updated successfully", "user_id": update_data.user_id, "new_position": update_data.position}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Error updating employee's position: {e}")
        raise HTTPException(status_code=500, detail="Error updating employee's position")

    finally:
        session.close()

