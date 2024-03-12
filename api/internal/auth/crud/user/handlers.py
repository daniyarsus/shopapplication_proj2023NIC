from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.services.auth.models import User
from api.internal.auth.crud.user.controllers import UserManager
from api.internal.auth.crud.user import schemas

router = APIRouter()


@router.post("/create-user")
async def create_employee_endpoint(create_data: schemas.CreateUser = Depends(),
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    user_manager = UserManager(current_user=current_user,
                               db=db)
    result = await user_manager.create_user(create_data=create_data)
    return result


@router.put("/update-user")
async def create_employee_endpoint(update_data: schemas.UpdateUser = Depends(),
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    user_manager = UserManager(current_user=current_user,
                               db=db)
    result = await user_manager.update_user(update_data=update_data)
    return result


@router.delete("/delete-user")
async def create_employee_endpoint(delete_data: schemas.DeleteUser = Depends(),
                                   db: AsyncSession = Depends(get_db),
                                   current_user: User = Depends(get_current_user)
                                   ):
    user_manager = UserManager(current_user=current_user,
                               db=db)
    result = await user_manager.delete_user(delete_data=delete_data)
    return result


@router.get("/get-all-user")
async def get_employee_endpoint(db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user)
                                ):
    user_manager = UserManager(current_user=current_user,
                               db=db)
    result = await user_manager.get_all_user()
    return result
