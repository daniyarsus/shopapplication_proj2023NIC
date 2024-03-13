from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.internal.auth.models import User
from api.internal.shop.models import Payment
from api.internal.shop.crud.payment import schemas


class PaymentManager:
    def __init__(self, current_user: User, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    async def create_payment(self, create_data: schemas.CreatePayment):
        try:
            payment = Payment(
                user_id=create_data.user_id,
                summ=create_data.summ,
                foods_id=create_data.foods_id,
                place=create_data.place,
                qr_code=create_data.qr_code,
                is_verified=create_data.is_verified,
                is_received=create_data.is_received
            )

            self.db.add(payment)
            await self.db.commit()

            return {"message": "Payment created successfully", "payment_id": payment.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_payment(self, update_data: schemas.UpdatePayment):
        try:
            query = select(Payment).where(Payment.id == update_data.id)
            result = await self.db.execute(query)
            payment = result.scalar_one_or_none()

            if payment:
                payment.user_id = update_data.user_id,
                payment.summ = update_data.summ,
                payment.foods_id = update_data.foods_id,
                payment.place = update_data.place,
                payment.qr_code = update_data.qr_code,
                payment.is_verified = update_data.is_verified,
                payment.is_received = update_data.is_received,
                payment.updated_at = datetime.utcnow()

                await self.db.commit()
                await self.db.refresh(payment)

                return {"message": "Payment updated successfully", "payment_id": payment.id}

            else:
                raise HTTPException(status_code=404, detail="Payment not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_payment(self, delete_data: schemas.DeletePayment):
        try:
            query = select(Payment).where(Payment.id == delete_data.id)
            result = await self.db.execute(query)
            payment = result.scalar_one_or_none()

            if payment:
                await self.db.delete(payment)
                await self.db.commit()

                return {"message": "Payment deleted successfully", "payment_id": payment.id}

            else:
                raise HTTPException(status_code=404, detail="Payment not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_payment(self):
        query = select(Payment)
        result = await self.db.execute(query)
        payment = result.scalars().all()
        payment_data = [
            {"id": payment.id,
             "user_id": payment.user_id,
             "summ": payment.summ,
             "foods_id": payment.foods_id,
             "place": payment.place,
             "qr_code": payment.qrcode,
             "is_verified": payment.is_verified,
             "is_received": payment.is_received
             }
            for payment in payment
        ]

        return payment_data
