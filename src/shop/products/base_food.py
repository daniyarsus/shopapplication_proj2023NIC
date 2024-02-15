from fastapi import HTTPException, status

from src.database.models import Assortment, FoodSet, Employee


class FoodManager:
    def __init__(self, current_user, db):
        self.current_user = current_user
        self.db = db

    async def _check_owner(self):
        employee = self.db.query(Employee).filter(
            Employee.user_id == self.current_user.id,
            Employee.position.lower() == "owner"
        ).first()
        if not employee:
            raise HTTPException(status_code=403, detail="You are not authorized to perform this operation")

    async def create_food(self, create_data):
        await self._check_owner()

        food = Assortment(
            name=create_data.name,
            description=create_data.description,
            price=create_data.price,
            type=create_data.type,
            image_bs64=create_data.image_bs64
        )
        self.db.add(food)
        self.db.commit()
        self.db.refresh(food)

        return {"message": "Food created successfully", "food_id": food.id}

    async def update_food(self, update_data):
        await self._check_owner()

        food = self.db.query(Assortment).filter(Assortment.id == update_data.food_id).first()
        if food:
            food.name = update_data.name
            food.description = update_data.description
            food.price = update_data.price
            food.type = update_data.type
            food.image_bs64 = update_data.image_bs64
            self.db.commit()
            return {"message": "Food updated successfully", "food_id": food.id}
        else:
            raise HTTPException(status_code=404, detail="Food not found")

    async def delete_food(self, delete_data):
        await self._check_owner()

        food = self.db.query(Assortment).filter(Assortment.id == delete_data.food_id).first()
        if food:
            self.db.delete(food)
            self.db.commit()
            return {"message": "Food deleted successfully", "food_id": delete_data.food_id}
        else:
            raise HTTPException(status_code=404, detail="Food not found")

    async def get_food(self):

        try:
            food = self.db.query(Assortment).all()
            return food
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.db.close()
