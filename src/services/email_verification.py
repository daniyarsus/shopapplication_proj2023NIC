from fastapi import HTTPException, Depends
import requests

from src.settings.config import DOMAIN_NAME, API_KEY, SessionLocal
from src.services.generate_code import generate_verification_code
from src.database.models import User
from src.validators.schemas import CheckCode, SendEmail


# Функция для отправки кода подтверждения
async def send_email(post_email: SendEmail):
    db = SessionLocal()
    code = generate_verification_code()
    existing_user = db.query(User).filter(User.email == post_email.email).first()

    # Проверка, что пользователь существует и не подтвержден
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if existing_user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    # Обновление кода подтверждения для пользователя
    existing_user.verification_code = code
    db.commit()

    try:
        # Отправка письма с кодом подтверждения
        response = requests.post(
            f"https://api.mailgun.net/v3/{DOMAIN_NAME}/messages",
            auth=("api", API_KEY),
            data={
                "from": f"Excited User <mailgun@{DOMAIN_NAME}>",
                "to": existing_user.email,
                "subject": "Код подтверждения для регистрации в приложение ...",
                "text": f"Ваш код подтверждения: {code}. Никому его не сообщайте!"
            })

        response.raise_for_status()
        return {"message": "Email sent successfully", "status": response.status_code}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


# Функция для проверки введенного кода
async def verification_code(check: CheckCode):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == check.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if check.code is None:
        raise HTTPException(status_code=400, detail="Code must be provided")
    if check.code != existing_user.verification_code:
        raise HTTPException(status_code=400, detail="Code does not match")

    # Подтверждение пользователя
    existing_user.is_verified = True
    db.commit()
    return {"message": "User has been verified"}

