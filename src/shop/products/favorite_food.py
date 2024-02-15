from fastapi import Depends, HTTPException, status

from src.database.models import User, FavoriteFood, Assortment


async def add_favorite_food(food_data, current_user, db):

    try:
        # Проверяем, существует ли блюдо
        food = db.query(Assortment).filter(Assortment.id == food_data.food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail="Food not found")

        # Проверяем, уже ли блюдо в избранном
        existing_favorite = db.query(FavoriteFood).filter(
            FavoriteFood.user_id == current_user.id,
            FavoriteFood.food_id == food_data.food_id
        ).first()
        if existing_favorite:
            raise HTTPException(status_code=400, detail="Food already in favorite")

        # Добавляем блюдо в избранное
        new_favorite = FavoriteFood(user_id=current_user.id, food_id=food_data.food_id)
        db.add(new_favorite)
        db.commit()
        return {"message": "Food added to favorite successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Закрываем сессию
        db.close()


async def delete_favorite_food(food_data, current_user, db):
    favorite = db.query(FavoriteFood).filter(
        FavoriteFood.user_id == current_user.id,
        FavoriteFood.food_id == food_data.food_id
    ).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite food not found")

    # Удаляем блюдо из избранного
    db.delete(favorite)
    db.commit()
    return {"message": "Food removed from favorite successfully"}


async def list_favorite_foods(current_user, db):
    try:
        favorites = db.query(FavoriteFood).filter(FavoriteFood.user_id == current_user.id).all()
        favorite_foods = []
        for favorite in favorites:
            food = db.query(Assortment).filter(Assortment.id == favorite.food_id).first()
            if food:
                food_info = {
                    "food_id": food.id,
                    "name": food.name,
                    "description": food.description,
                    "price": food.price,
                    "type": food.type,
                    "image_url": food.image_url
                }
                favorite_foods.append(food_info)
        return favorite_foods
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


