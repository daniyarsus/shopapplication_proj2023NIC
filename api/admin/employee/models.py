from sqladmin import ModelView

from api.internal.management.models import Employee


class EmployeeAdmin(ModelView, model=Employee):
    column_list = ['id', 'user_id', 'username', 'added_on', 'changed_on', 'permission']
