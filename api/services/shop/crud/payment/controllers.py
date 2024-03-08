from datetime import datetime

import qrcode
from io import BytesIO
import base64

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.shop.models import AssortmentFood, Payment
from api.services.auth.models import User
from api.services.shop.crud.payment import schemas


class PaymentManager:
    def __init__(self, current_user: User, db: AsyncSession) -> None:
        self.db = db
        self.current_user = current_user

    async def _calculate_total_price(self, foods_id):
        if not foods_id:
            raise HTTPException(status_code=404, detail="Список блюд не может быть пустым.")

        query = select(AssortmentFood).where(AssortmentFood.id.in_(foods_id))
        results = await self.db.execute(query)

        total_price = sum(food.price for food in (await results.scalars().all()))
        return total_price

    async def _generate_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_encoded_result_bytes = base64.b64encode(img_byte_arr)
        base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')

        return f"data:image/png;base64,{base64_encoded_result_str}"

    async def create_payment(self, payment_data: schemas.PaymentCreate):
        try:
            total_price = await self._calculate_total_price(payment_data.foods_id)

            new_payment = Payment(
                user_id=self.current_user.id,
                foods_id=payment_data.foods_id,
                summ=total_price,
                place=payment_data.place,
            )

            self.db.add(new_payment)
            await self.db.commit()
            await self.db.refresh(new_payment)

            payment_data = {
                "user_id": self.current_user.id,
                "foods_id": payment_data.foods_id,
                "summ": total_price,
                "place": payment_data.place
            }

            qr_data = str(payment_data)
            qr_code = await self._generate_qr_code(qr_data)

            await self.db.commit()
            await self.db.refresh(new_payment)

            return {"message": "Payment created successfully", "total": total_price, "qr_code": qr_code}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_payments(self):
        try:
            query = select(Payment).where(Payment.user_id == self.current_user.id)
            result = await self.db.execute(query)
            payments = result.scalars().all()

            return payments

            #favorite_foods = []
            #for payment in payments:
            #    query = select(Payment).where(Payment.id == payments.food_id)
            #    result = await self.db.execute(query)
            #    food = result.scalar_one_or_none()
#
            #    if food:
            #        food_info = {
            #            "food_id": food.id,
            #            "food_name": food.name,
            #            "food_description": food.description,
            #            "food_type": food.type,
            #            "food_price": food.price
            #        }
            #        favorite_foods.append(food_info)

            #return favorite_foods

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
