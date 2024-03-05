from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.internal.auth.models import User
from api.internal.shop.models import AssortmentFood
from api.internal.shop.crud.assortment import schemas


class FoodManager:
    def __init__(self, current_user: User, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    async def create_food(self, create_data: schemas.CreateAssortmentFood):
        try:
            food = AssortmentFood(
                name=create_data.name,
                description=create_data.description,
                price=create_data.price,
                type=create_data.type
            )

            self.db.add(food)
            await self.db.commit()

            return {"message": "Food created successfully", "food_id": food.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_food(self, update_data: schemas.UpdateAssortmentFood):
        try:
            query = select(AssortmentFood).where(AssortmentFood.id == update_data.id)
            result = await self.db.execute(query)
            food = result.scalar_one_or_none()

            if food:
                food.name = update_data.name
                food.description = update_data.description
                food.price = update_data.price
                food.type = update_data.type
                food.changed_on = datetime.utcnow()

                await self.db.commit()
                await self.db.refresh(food)

                return {"message": "Food updated successfully", "food_id": food.id}

            else:
                raise HTTPException(status_code=404, detail="Food not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_food(self, delete_data: schemas.DeleteAssortmentFood):
        try:
            query = select(AssortmentFood).where(AssortmentFood.id == delete_data.id)
            result = await self.db.execute(query)
            food = result.scalar_one_or_none()

            if food:
                await self.db.delete(food)
                await self.db.commit()

                return {"message": "Food deleted successfully", "food_id": delete_data.id}

            else:
                raise HTTPException(status_code=404, detail="Food not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_food(self):
        query = select(AssortmentFood)
        result = await self.db.execute(query)
        food = result.scalars().all()
        food_data = [
            {"id": food.id,
             "name": food.name,
             "description": food.description,
             "price": food.price,
             "type": food.type}
            for food in food
        ]

        return food_data
