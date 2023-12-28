import jwt
from fastapi import HTTPException, Depends

from src.settings.config import oauth2_scheme, SECRET_KEY, ALGORITHM, SessionLocal
from src.database.models import User


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

