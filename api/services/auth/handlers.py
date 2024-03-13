from fastapi import (APIRouter,
                     Depends)
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.dependencies.db import get_db
from api.utils.dependencies.current_user import get_current_user
from api.services.auth.models import User

from api.services.auth.crud.signin.controllers import SigninManager
from api.services.auth.crud.signin.schemas import SigninSchema

from api.services.auth.crud.signup.controllers import SignupManager
from api.services.auth.crud.signup.schemas import SignupSchema


auth_router = APIRouter()


@auth_router.post("/registration")
async def register_user_endpoint(form_data: SignupSchema = Depends(),
                       db: AsyncSession = Depends(get_db)):
    signup_manager = SignupManager(form_data, db)
    result = await signup_manager.register_user()
    return result


@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: AsyncSession = Depends(get_db)):
    signin_manager = SigninManager(form_data, db)
    result = await signin_manager.authenticate_user()
    return result


@auth_router.post("/signup/send-code")
async def verify_user_endpoint():
    ...


@auth_router.post("/signup/verify-code")
async def verify_user_endpoint():
    ...


@auth_router.post("/change-password/send-code")
async def change_password_endpoint():
    ...


@auth_router.post("/change-password/verify-code")
async def change_password_endpoint():
    ...
