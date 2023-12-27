from fastapi import Depends, HTTPException, APIRouter

from src.config.dependencies import get_current_user
from config.settings import SessionLocal
from schemas import QueueAdd, QueueReady
from src.database.models import *


queue_router = APIRouter()


# Эндпоинт для добавления в очередь
@queue_router.post("/add")
async def add_to_queue(queue_add: QueueAdd, current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    # Проверяем, существует ли уже запись в очереди для текущего пользователя и магазина
    existing_queue_item = session.query(QueueItem).filter(
        QueueItem.user_id == current_user.id,
        QueueItem.is_order_ready == False  # Проверка, что заказ еще не готов
    ).first()

    if existing_queue_item:
        session.close()
        raise HTTPException(status_code=400, detail="User is already in the queue")

    # Проверяем, существует ли блюдо с указанным ID
    dish = session.query(Dish).filter(Dish.id == queue_add.dish_id).first()
    if not dish:
        session.close()
        raise HTTPException(status_code=404, detail="Dish not found")

    # Создаем запись в очереди
    queue_item = QueueItem(user_id=current_user.id, shop_id=dish.shop_id)
    session.add(queue_item)
    session.commit()
    session.refresh(queue_item)

    # Закрываем сессию
    session.close()

    return {"queue_id": queue_item.id, "message": "You've been added to the queue"}


@queue_router.post("/ready")
async def order_ready(queue_ready: QueueReady, current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    # Проверяем, привязан ли текущий пользователь к выбранному магазину
    if current_user.shop_id != queue_ready.shop_id:
        raise HTTPException(status_code=403, detail="You are not allowed to mark orders as ready for this shop")

    # Получаем запись в очереди
    queue_item = session.query(QueueItem).filter(
        QueueItem.id == queue_ready.queue_id,
        QueueItem.shop_id == queue_ready.shop_id,
        QueueItem.is_order_ready == False  # Проверка, что заказ еще не готов
    ).first()

    if not queue_item:
        session.close()
        raise HTTPException(status_code=404, detail="Queue item not found")

    # Помечаем заказ как готовый
    queue_item.is_order_ready = True
    session.commit()

    # Закрываем сессию
    session.close()

    return {"queue_id": queue_ready.queue_id, "message": "Order is ready for pickup"}


# Измененный эндпоинт для проверки статуса очереди у магазина
@queue_router.get("/status")
async def check_shop_queue_status(current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    shop = session.query(Shop).filter(Shop.id == current_user.shop_id).first()

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Получаем все записи в очереди для данного магазина с информацией о пользователе,
    # отсортированные в обратном порядке
    shop_queue_status = session.query(QueueItem, User).join(User).filter(
        QueueItem.shop_id == shop.id
    ).order_by(QueueItem.id.desc()).all()

    # Закрываем сессию
    session.close()

    # Формируем результат, включая username пользователя в очереди
    result = [{"queue_id": queue_item.id, "is_order_ready": queue_item.is_order_ready, "username": user.username} for
              queue_item, user in shop_queue_status]

    return result


@queue_router.get("/my_queue_status")
async def my_queue_status(current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    # Получаем все записи в очереди для текущего пользователя, отсортированные в обратном порядке
    user_queue_status = session.query(QueueItem).filter(QueueItem.user_id == current_user.id).order_by(
        QueueItem.id.desc()).first()

    # Закрываем сессию
    session.close()

    return user_queue_status
