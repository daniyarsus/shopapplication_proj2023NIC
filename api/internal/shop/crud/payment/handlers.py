from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.decorators.permission import permission_required
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.internal.auth.models import User
from api.internal.shop.crud.payment import schemas
from api.internal.shop.crud.payment.controllers import PaymentManager

router = APIRouter()


@router.post("/create-payment")
@permission_required(2)
async def create_payment_endpoint(create_data: schemas.CreatePayment = Depends(),
                                  db: AsyncSession = Depends(get_db),
                                  current_user: User = Depends(get_current_user)
                                  ):
    payment_manager = PaymentManager(current_user=current_user,
                                     db=db)
    result = await payment_manager.create_payment(create_data=create_data)
    return result


@router.put("/update-payment")
@permission_required(2)
async def update_payment_endpoint(update_data: schemas.UpdatePayment = Depends(),
                                  db: AsyncSession = Depends(get_db),
                                  current_user: User = Depends(get_current_user)
                                  ):
    payment_manager = PaymentManager(current_user=current_user,
                                     db=db)
    result = await payment_manager.update_payment(update_data=update_data)
    return result


@router.delete("/delete-payment")
@permission_required(2)
async def delete_payment_endpoint(delete_data: schemas.DeletePayment = Depends(),
                                  db: AsyncSession = Depends(get_db),
                                  current_user: User = Depends(get_current_user)
                                  ):
    payment_manager = PaymentManager(current_user=current_user,
                                     db=db)
    result = await payment_manager.delete_payment(delete_data=delete_data)
    return result


@router.get("/get-all-payment")
@permission_required(1)
async def get_payment_endpoint(db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user)
                               ):
    payment_manager = PaymentManager(current_user=current_user,
                                     db=db)
    result = await payment_manager.get_all_payment()
    return result
