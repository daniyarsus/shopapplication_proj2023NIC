from fastapi import FastAPI, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as redis

from src.settings.config import REDIS_URL_FOR_CACHE
from src.services.redis_utils.redis_activate import init_redis, init_redis_cache
from src.services.postgres_utils.postgres_activate import init_postgres
from src.routers import api_router


app = FastAPI(
    title="DoughJoy Delights API",
    description="API for DoughJoy Delights",
    contact={"name": "Hui",
             "email": "daniyar.kanu@gmail.com",
             "x-telegram": "danyaKex"},
    version="1.0.0",
    docs_url="/api/v1/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import asyncio

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from api.db.database import Base, sync_session, settings, engine
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db


from api.services.user.models import User
from api.services.user.auth.signup.schemas import UserCreate


from pydantic import BaseModel


class VacancyCreate(BaseModel):
    name: str
    description: str


app: FastAPI = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user


class UpdateUser(BaseModel):
    username: str
    password: str
    university: str


@app.post("/token")
async def login_user(username, password):
    return {
            "username": username,
            "password": password
    }


@app.put("/update_user")
def update_user_profile(username: str, university: str, email: str, description: str):
    return {
        "username": username,
        "university": university,
        "description": description
    }


@app.get("/get_student_info")
def get_student_info(student_id: int):
    return {"student_id": student_id}


@app.post("/create_vacancy")
def create_vacancy(vacancy: VacancyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Only employers can create vacancies")
    new_vacancy = Vacancy(**vacancy.dict(), employer_id=current_user.id)
    db.add(new_vacancy)
    db.commit()
    db.refresh(new_vacancy)
    return new_vacancy


@app.put("/update_vacancy")
def update_vacancy(name: str, description: str):
    return {
        "name": name,
        "description": description
    }


@app.delete("/delete_vacancy")
def delete_vacancy(id: int):
    return {
        "id": id
    }


@app.get("/get-all-vacancies")
def get_all_vacancies():
    return {
        "vacancies": [{"python backend": 1}, {"java spring": 3}],
        }


@app.post("/verify-vacancy")
def verify_vacancy(student_id: int, vacancy_id, choise: bool):
    return {
            "student_id": student_id,
            "vacancy_id": vacancy_id,
            "choise": choise
           }


@app.get("/secret")
async def get_secret(current_user: User = Depends(get_current_user)):
    return current_user


@app.on_event("startup")
async def startup() -> None:
    Base.metadata.create_all(bind=engine)

