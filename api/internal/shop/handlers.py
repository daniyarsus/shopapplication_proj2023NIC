from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.decorators.permission import permission_required
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.services.auth.models import User
from api.internal.shop.crud.assortment.schemas import (CreateAssortmentBaseFood,
                                                       UpdateAssortmentBaseFood,
                                                       DeleteAssortmentBaseFood,
                                                       CreateAssortmentSetFood,
                                                       UpdateAssortmentSetFood,
                                                       DeleteAssortmentSetFood
                                                       )
from api.internal.shop.crud.assortment.controllers import (BaseFoodManager,
                                                           SetFoodManager)

shop_router = APIRouter()


@shop_router.post("/create-base-food")
async def create_base_food_endpoint(create_data: CreateAssortmentBaseFood,
                                    db: AsyncSession = Depends(get_db),
                                    current_user: User = Depends(get_current_user)
                                    ):
    base_food_manager = BaseFoodManager(current_user=current_user,
                                        db=db)
    result = await base_food_manager.create_base_food(create_data=create_data)
    return result


@shop_router.put("/update-base-food")
async def update_base_food_endpoint(update_data: UpdateAssortmentBaseFood,
                                    db: AsyncSession = Depends(get_db),
                                    current_user: User = Depends(get_current_user)
                                    ):
    base_food_manager = BaseFoodManager(current_user=current_user,
                                        db=db)
    result = await base_food_manager.update_base_food(update_data=update_data)
    return result


@shop_router.delete("delete-base-food")
async def delete_base_food_endpoint(delete_data: DeleteAssortmentBaseFood,
                                    db: AsyncSession = Depends(get_db),
                                    current_user: User = Depends(get_current_user)
                                    ):
    base_food_manager = BaseFoodManager(current_user=current_user,
                                        db=db)
    result = await base_food_manager.delete_base_food(delete_data=delete_data)
    return result


@shop_router.get("get-base-food")
async def get_base_food_endpoint(db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(get_current_user)
                                 ):
    base_food_manager = BaseFoodManager(current_user=current_user,
                                        db=db)
    result = await base_food_manager.get_all_base_food()
    return result


@shop_router.post("/create-set-food")
async def create_set_food_endpoint(create_data: CreateAssortmentSetFood,
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    set_food_manager = SetFoodManager(current_user=current_user,
                                      db=db)
    result = await set_food_manager.create_set_food(create_data=create_data)
    return result


@shop_router.put("/update-set-food")
async def update_set_food_endpoint(update_data: UpdateAssortmentSetFood,
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    set_food_manager = SetFoodManager(current_user=current_user,
                                      db=db)
    result = await set_food_manager.update_set_food(update_data=update_data)
    return result


@shop_router.delete("/delete-set-food")
async def delete_set_food_endpoint(delete_data: DeleteAssortmentBaseFood,
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    set_food_manager = SetFoodManager(current_user=current_user,
                                      db=db)
    result = await set_food_manager.delete_set_food(delete_data=delete_data)
    return result


@shop_router.get("/get-set-food")
async def get_base_food_endpoint(db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(get_current_user)
                                 ):
    set_food_manager = SetFoodManager(current_user=current_user,
                                      db=db)
    result = await set_food_manager.get_all_set_food()
    return result
