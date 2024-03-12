from sqladmin import ModelView

from api.services.shop.models import AssortmentFood


class AssortmentFoodAdmin(ModelView, model=AssortmentFood):
    column_list = [col.key for col in AssortmentFood.__table__.columns]
