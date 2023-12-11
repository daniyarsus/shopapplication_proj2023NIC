from fastapi import Depends, HTTPException, status, Response, APIRouter

from src.config.dependencies import get_current_user
from src.config.settings import SessionLocal
from src.schemas.validators import ShopCreate, ShopMenuRequest
from src.database.models import *


shop_router = APIRouter()


@shop_router.post("/create")
async def create_shop(shop_create: ShopCreate, current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Проверяем, владеет ли пользователь уже магазином
        if current_user.owned_shops:
            raise HTTPException(status_code=400, detail="User already owns a shop")

        existing_shop = session.query(Shop).filter(Shop.name == shop_create.name).first()
        if existing_shop:
            raise HTTPException(status_code=400, detail="Shop already exists")

        new_shop = Shop(name=shop_create.name, owner_id=current_user.id)
        session.add(new_shop)
        session.commit()

        # Обновляем shop_id для пользователя с таким же ID, что и у current_user
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            user.shop_id = new_shop.id
            session.commit()

        return {"shop_id": new_shop.id, "name": new_shop.name}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


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


@shop_router.delete("/delete_shop")
async def delete_shop(current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    try:
        # Находим магазин, привязанный к пользователю
        shop = session.query(Shop).filter(Shop.id == current_user.shop_id).first()

        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")

        # Проверяем, является ли пользователь владельцем магазина
        if shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to delete this shop")

        # Удаляем магазин
        session.delete(shop)
        session.commit()
        return {"message": "Shop deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()