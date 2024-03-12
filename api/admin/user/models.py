from sqladmin import ModelView

from api.services.auth.models import User


class UserAdmin(ModelView, model=User):
    column_list = [col.key for col in User.__table__.columns]