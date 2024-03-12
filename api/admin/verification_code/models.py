from sqladmin import ModelView

from api.services.auth.models import VerificationCode


class VerificationCodeAdmin(ModelView, model=VerificationCode):
    column_list = [col.key for col in VerificationCode.__table__.columns]
