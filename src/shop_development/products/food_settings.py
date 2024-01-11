from fastapi import Depends, HTTPException, status

from src.settings.config import SessionLocal
from src.database.models import User, Employee, Assortment, FoodSet
from typing import List


async def create_food(new_food, current_user):
    db = SessionLocal()
    # Проверяем, что пользователь - админ
    employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
    if not employee or employee.position.lower() != "owner":
        raise HTTPException(status_code=403, detail="You are not employee to create food items.")

    # Создаем новое блюдо
    new_food = Assortment(
        name=new_food.name,
        description=new_food.description,
        price=new_food.price,
        type=new_food.type
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return {"message": "Food created successfully", "food_id": new_food.id}


async def update_food(food_data, current_user):
    db = SessionLocal()
    # Проверяем, что пользователь - админ
    employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
    if not employee or employee.position.lower() != "owner":
        raise HTTPException(status_code=403, detail="You are not authorized to update food items.")

    # Находим и обновляем блюдо
    food = db.query(Assortment).filter(Assortment.id == food_data.food_id).first()
    if food:
        food.name = food_data.name
        food.description = food_data.description
        food.price = food_data.price
        food.type = food_data.type
        db.commit()
        return {"message": "Food updated successfully", "food_id": food.id}
    else:
        raise HTTPException(status_code=404, detail="Food not found")


async def delete_food(del_food, current_user):
    db = SessionLocal()
    # Проверяем, что пользователь - админ
    employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
    if not employee or employee.position.lower() != "owner":
        raise HTTPException(status_code=403, detail="You are not authorized to delete food items.")

    # Находим и удаляем блюдо
    food = db.query(Assortment).filter(Assortment.id == del_food.food_id).first()
    if food:
        db.delete(food)
        db.commit()
        return {"message": "Food deleted successfully", "food_id": del_food.food_id}
    else:
        raise HTTPException(status_code=404, detail="Food not found")


async def create_food_set(food_set, current_user):
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
        if not employee or employee.position.lower() != "owner":
            raise HTTPException(status_code=403, detail="You are not authorized to create food sets.")

        new_food_set = FoodSet(
            name=food_set.name,
            description=food_set.description,
            price=food_set.price
        )
        db.add(new_food_set)
        db.commit()
        db.refresh(new_food_set)

        return {
            "message": "Food set created successfully",
            "food_set_id": new_food_set.id,
            "name": new_food_set.name,
            "description": new_food_set.description,
            "price": new_food_set.price
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
