from datetime import datetime
import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.settings.config import DOMAIN_NAME, API_KEY, SessionLocal
from src.database.models import User, VerificationCode
from src.validators.schemas import SendEmail
from src.services.generate_code import generate_verification_code


async def send_email(post_email):
    db = SessionLocal()
    code = generate_verification_code()
    existing_user = db.query(User).filter(User.email == post_email.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if existing_user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    new_verification_code = VerificationCode(
        user_id=existing_user.id,
        email_code=code,
        email_verified_at=datetime.utcnow()
    )

    db.add(new_verification_code)
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


async def verification_code(check):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == check.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Находим последний код верификации для пользователя
    verification_record = db.query(VerificationCode)\
        .filter(VerificationCode.user_id == existing_user.id)\
        .order_by(VerificationCode.email_verified_at.desc()).first()

    if not verification_record:
        raise HTTPException(status_code=404, detail="Verification code not found")

    if datetime.utcnow() - verification_record.email_verified_at > timedelta(minutes=1):
        raise HTTPException(status_code=400, detail="Verification code has expired")

    if check.code is None or not verification_record:
        raise HTTPException(status_code=400, detail="Code must be provided")
    if check.code != verification_record.email_code:
        raise HTTPException(status_code=400, detail="Code does not match")

    existing_user.is_verified = True
    db.commit()
    return {"message": "User has been verified"}

