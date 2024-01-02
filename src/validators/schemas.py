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


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class VerifyAndNewPassword(BaseModel):
    email: EmailStr
    code: str
    new_password: str


class NewEmployee(BaseModel):
    user_id: int


class UpdatePosition(BaseModel):
    user_id: int
    position: str


class DeleteEmployee(BaseModel):
    user_id: int

