from api.internal.auth.models import User
from api.database.database import async_engine, Base

from sqladmin import Admin, ModelView

admin = Admin(app, async_engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]


admin.add_view(UserAdmin)
