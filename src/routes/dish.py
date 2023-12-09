from fastapi import Depends, HTTPException, status, Response, APIRouter

from src.config.dependencies import get_current_user
from src.config.settings import SessionLocal
from src.schemas.validators import DishCreate
from src.database.models import *


dish_router = APIRouter()


# Dish endpoints
@dish_router.post("/create")
async def create_dish(dish_create: DishCreate, current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    shop = session.query(Shop).filter(Shop.id == current_user.shop_id).first()

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Проверяем, привязан ли текущий пользователь к выбранному магазину
    if current_user.shop_id != shop.id:
        raise HTTPException(status_code=403, detail="You are not allowed to create dishes for this shop")

    dish = Dish(name=dish_create.name, shop_id=shop.id)
    session.add(dish)
    session.commit()
    return {"dish_id": dish.id, "name": dish.name, "shop_id": dish.shop_id}
