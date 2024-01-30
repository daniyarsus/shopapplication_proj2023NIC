from fastapi import Depends, HTTPException, status

from src.settings.config import SessionLocal
from src.database.models import User, Employee, Assortment, FoodSet, Payments


async def calculate_total_price(foods_id, sets_id, db):
    # Расчет общей стоимости для отдельных блюд
    total_price = 0
    if foods_id:
        for food_id in foods_id:
            food = db.query(Assortment).filter(Assortment.id == food_id).first()
            if food:
                total_price += food.price
            else:
                raise HTTPException(status_code=404, detail=f"Food with id {food_id} not found")

    # Расчет общей стоимости для наборов блюд
    if sets_id:
        for set_id in sets_id:
            food_set = db.query(FoodSet).filter(FoodSet.id == set_id).first()
            if food_set:
                total_price += food_set.price
            else:
                raise HTTPException(status_code=404, detail=f"Food set with id {set_id} not found")

    return total_price


async def create_payment(payment_data, current_user):
    db = SessionLocal()
    try:
        # Вычисляем общую стоимость
        total_price = await calculate_total_price(payment_data.foods_id, payment_data.sets_id, db)

        # Создаем запись о платеже
        new_payment = Payments(
            buyer_id=current_user.id,
            foods_id=payment_data.foods_id,
            sets_id=payment_data.sets_id,
            total=total_price,
            place=payment_data.place
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        return {"message": "Payment created successfully", "total": total_price}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
