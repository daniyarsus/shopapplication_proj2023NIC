from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.shop.models import (FavoriteFood,
                                      AssortmentFood)
from api.services.auth.models import User
from api.services.shop.crud.favorite_food import schemas


class FavoriteFoodManager:
    def __init__(self, current_user: User, db: AsyncSession) -> None:
        self.current_user = current_user
        self.db = db

    async def add_favorite_food(self, create_data: schemas.AddFavoriteFood):
        try:
            favorite = FavoriteFood(
                user_id=self.current_user.id,
                food_id=create_data.id
            )

            self.db.add(favorite)
            await self.db.commit()

            return {"message": "Favorite food created successfully", "id": favorite.id}

        except HTTPException as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def remove_favorite_food(self, delete_data: schemas.DeleteFavoriteFood):
        try:
            query = delete(FavoriteFood).where(FavoriteFood.food_id == delete_data.id,
                                               FavoriteFood.user_id == self.current_user.id)
            result = await self.db.execute(query)

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Favorite food not found")

            await self.db.commit()

            return {"message": "Favorite food deleted successfully", "id": delete_data.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_favorite_food(self):
        try:
            query = select(FavoriteFood).where(FavoriteFood.user_id == self.current_user.id)
            result = await self.db.execute(query)
            favorites = result.scalars().all()

            favorite_foods = []
            for favorite in favorites:
                query = select(AssortmentFood).where(AssortmentFood.id == favorite.food_id)
                result = await self.db.execute(query)
                food = result.scalar_one_or_none()

                if food:
                    food_info = {
                        "food_id": food.id,
                        "food_name": food.name,
                        "food_description": food.description,
                        "food_type": food.type,
                        "food_price": food.price
                    }
                    favorite_foods.append(food_info)

            return favorite_foods

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
