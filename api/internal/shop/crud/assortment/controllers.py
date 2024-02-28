from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.auth.models import User
from api.services.shop.models import AssortmentBaseFood, AssortmentSetFood


class BaseFoodManager:
    def __init__(self, current_user: User, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    async def create_base_food(self, create_data):
        try:
            food = AssortmentBaseFood(
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

    async def update_base_food(self, update_data):
        try:
            query = update(AssortmentBaseFood).where(AssortmentBaseFood.id == update_data.id)
            result = await self.db.execute(query)
            food = result.scalar_one_or_none()

            if food:
                food.name = update_data.name
                food.description = update_data.description
                food.price = update_data.price
                food.type = update_data.type
                food.changed_on = datetime.utcnow

                await self.db.commit()
                await self.db.refresh(food)

                return {"message": "Food updated successfully", "food_id": food.id}

            else:
                raise HTTPException(status_code=404, detail="Food not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_base_food(self, delete_data):
        try:
            query = delete(AssortmentBaseFood).where(AssortmentBaseFood.id == delete_data.id)
            result = await self.db.execute(query)
            food = result.scalar_one_or_none()

            if food:
                await self.db.delete(food)
                await self.db.commit()

                return {"message": "Food deleted successfully", "food_id": delete_data.food_id}

            else:
                raise HTTPException(status_code=404, detail="Food not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_base_food(self):
        query = select(AssortmentBaseFood)
        result = await self.db.execute(query)
        food_set = result.all()

        return food_set


class SetFoodManager:
    def __init__(self, current_user: User, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    async def create_set_food(self, create_data):
        try:
            food_set = AssortmentSetFood(
                name=create_data.name,
                foods_id=create_data.foods_id,
                description=create_data.description,
                price=create_data.price
            )
            self.db.add(food_set)
            await self.db.commit()

            return {
                "message": "Food set created successfully",
                "food_set_id": food_set.id,
                "name": food_set.name,
                "description": food_set.description,
                "price": food_set.price
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_set_food(self, update_data):
        try:
            query = update(AssortmentSetFood).where(AssortmentSetFood.id == update_data.id)
            result = await self.db.execute(query)
            food_set = result.scalar_one_or_none()

            if food_set:
                food_set.name = update_data.name
                food_set.foods_id = update_data.foods_id
                food_set.description = update_data.description
                food_set.price = update_data.price
                food_set.changed_on = datetime.utcnow

                await self.db.commit()
                await self.db.refresh(food_set)

                return {
                    "message": "Food set updated successfully",
                    "food_set_id": food_set.id,
                    "name": food_set.name,
                    "description": food_set.description,
                    "price": food_set.price
                }

            else:
                raise HTTPException(status_code=404, detail="Food set not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_set_food(self, delete_data):
        try:
            query = delete(AssortmentSetFood).where(AssortmentSetFood.id == delete_data.id)
            result = await self.db.execute(query)
            food_set = result.scalar_one_or_none()

            if food_set:
                await self.db.delete(food_set)
                await self.db.commit()
                return {"message": "Food set deleted successfully", "food_set_id": delete_data.id}
            else:
                raise HTTPException(status_code=404, detail="Food set not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_set_food(self):
        try:
            query = select(AssortmentSetFood)
            result = await self.db.execute(query)
            food_set = result.all()

            return food_set

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
