from sqladmin import ModelView

from api.services.shop.models import Payment


class PaymentAdmin(ModelView, model=Payment):
    column_list = [col.key for col in Payment.__table__.columns]
