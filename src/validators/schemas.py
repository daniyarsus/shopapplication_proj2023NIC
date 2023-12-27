from pydantic import BaseModel, EmailStr, validator


class UserRegister(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    phone_number: str
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class SendEmail(BaseModel):
    email: EmailStr


class CheckCode(BaseModel):
    email: EmailStr
    code: str

