from fastapi import Depends, HTTPException, status, Response, APIRouter

from config.dependencies import get_current_user
from schemas.validators import ShopCreate, ShopMenuRequest
from database.models import *


shop_router = APIRouter()


# Shop endpoints
@shop_router.post("/create")
async def create_shop(shop_create: ShopCreate, current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    # Проверка, является ли текущий пользователь авторизованным
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    existing_shop = session.query(Shop).filter(Shop.name == shop_create.name).first()
    if existing_shop:
        raise HTTPException(status_code=400, detail="Shop already exists")

    shop = Shop(name=shop_create.name)
    session.add(shop)
    session.commit()
    return {"shop_id": shop.id, "name": shop.name}


@shop_router.post("/shop/menu")
async def get_menu(shop_menu_request: ShopMenuRequest):
    session = SessionLocal()

    # Получаем все блюда для конкретного магазина
    menu_items = session.query(Dish).filter(Dish.shop_id == shop_menu_request.shop_id).all()

    # Закрываем сессию
    session.close()

    # Формируем результат
    result = [{"dish_id": item.id, "name": item.name, "shop_id": item.shop_id} for item in menu_items]

    return result