from sqladmin import ModelView

from api.services.shop.models import FavoriteFood


class FavoriteFoodAdmin(ModelView, model=FavoriteFood):
    column_list = [col.key for col in FavoriteFood.__table__.columns]
