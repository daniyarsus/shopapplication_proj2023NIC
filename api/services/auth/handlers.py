from fastapi import (APIRouter,
                     Depends)
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.dependencies.db import get_db
from api.utils.dependencies.current_user import get_current_user
from api.services.auth.models import User

from api.services.auth.signin.controllers import SigninManager

from api.services.auth.signup.controllers import SignupManager
from api.services.auth.signup.schemas import SignupSchema


auth_router = APIRouter()


@auth_router.post("/registration")
async def registration(form_data: SignupSchema,
                       db: AsyncSession = Depends(get_db)):
    signup_manager = SignupManager(form_data, db)
    result = await signup_manager.register_user()
    return result


@auth_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    signin_manager = SigninManager(form_data, db)
    result = await signin_manager.authenticate_user()
    return result


#@auth_router.post("/refresh-token", response_model=TokenRefreshSchema)
#async def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_session)):
#    try:
#        return await RefreshTokenManager.refresh(refresh_token)
#    except HTTPException as e:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/secret")
async def secret(current_user: User = Depends(get_current_user)):
    return current_user.username

