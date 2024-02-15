from fastapi import HTTPException, status

from src.database.models import Assortment, FoodSet, Employee


class FoodSetManager:
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

    async def create_food_set(self, create_data):
        await self._check_owner()

        new_food_set = FoodSet(
            name=create_data.name,
            foods_id=create_data.foods_id,
            description=create_data.description,
            price=create_data.price,
            image_bs64=create_data.image_bs64
        )
        self.db.add(new_food_set)
        self.db.commit()
        self.db.refresh(new_food_set)

        return {
            "message": "Food set created successfully",
            "food_set_id": new_food_set.id,
            "name": new_food_set.name,
            "description": new_food_set.description,
            "price": new_food_set.price
        }

    async def update_food_set(self, update_data):
        await self._check_owner()

        food_set = self.db.query(FoodSet).filter(FoodSet.id == update_data.id).first()
        if food_set:
            food_set.name = update_data.name
            food_set.foods_id = update_data.foods_id
            food_set.description = update_data.description
            food_set.price = update_data.price
            food_set.image_bs64 = update_data.image_bs64
            self.db.commit()
            return {
                "message": "Food set updated successfully",
                "food_set_id": food_set.id,
                "name": food_set.name,
                "description": food_set.description,
                "price": food_set.price
            }
        else:
            raise HTTPException(status_code=404, detail="Food set not found")

    async def delete_food_set(self, delete_data):
        await self._check_owner()

        food_set = self.db.query(FoodSet).filter(FoodSet.id == delete_data.id).first()
        if food_set:
            self.db.delete(food_set)
            self.db.commit()
            return {"message": "Food set deleted successfully", "food_set_id": delete_data.id}
        else:
            raise HTTPException(status_code=404, detail="Food set not found")

    async def get_food_set(self):

        try:
            food_sets = self.db.query(FoodSet).all()
            return food_sets
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.db.close()
