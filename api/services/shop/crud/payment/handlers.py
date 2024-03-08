from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.decorators.permission import permission_required
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.services.auth.models import User

from api.services.shop.crud.payment.controllers import PaymentManager
from api.services.shop.crud.payment import schemas

router = APIRouter()


@router.post("/create-payment")
async def create_payment_endpoint(create_data: schemas.PaymentCreate = Depends(),
                                  current_user: User = Depends(get_current_user),
                                  db: AsyncSession = Depends(get_db),
                                  ):
    payment_manager = PaymentManager(current_user=current_user,
                                     db=db)
    result = await payment_manager.create_payment(payment_data=create_data)
    return result


@router.get("/get-all-payments")
async def get_all_payments_endpoint(current_user: User = Depends(get_current_user),
                                    db: AsyncSession = Depends(get_db)
                                    ):
    payment_manager = PaymentManager(current_user=current_user,
                                     db=db)
    result = await payment_manager.get_all_payments()
    return result

