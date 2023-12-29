from datetime import datetime
import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from src.settings.config import DOMAIN_NAME, API_KEY, SessionLocal
from src.database.models import User, VerificationCode
from src.services.generate_code import generate_verification_code


async def send_email_forgotten_password(email_send):
    db = SessionLocal()
    code = generate_verification_code()
    existing_user = db.query(User).filter(User.email == email_send.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not existing_user.is_verified:
        raise HTTPException(status_code=400, detail="Email is not verified")

    verification_code = db.query(VerificationCode).filter(VerificationCode.user_id == existing_user.id).first()
    if verification_code:
        # Обновляем код и время, если запись найдена
        verification_code.password_code = code
        verification_code.password_verified_at = datetime.utcnow()
    else:
        # Создаем новую запись, если пользователь не найден
        verification_code = VerificationCode(
            user_id=existing_user.id,
            password_code=code,
            password_verified_at=datetime.utcnow()
        )
        db.add(verification_code)

    db.commit()

    try:
        # Отправка письма с кодом подтверждения
        response = requests.post(
            f"https://api.mailgun.net/v3/{DOMAIN_NAME}/messages",
            auth=("api", API_KEY),
            data={
                "from": f"Excited User <mailgun@{DOMAIN_NAME}>",
                "to": existing_user.email,
                "subject": "test application",
                "text": f"for email {code}"
            })
        response.raise_for_status()
        return {"message": "Email sent successfully", "status": response.status_code}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


async def reset_password(verify_new_password):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == verify_new_password.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Находим последний код верификации для пользователя
    verification_record = db.query(VerificationCode)\
        .filter(VerificationCode.user_id == existing_user.id)\
        .order_by(VerificationCode.password_verified_at.desc()).first()

    if not verification_record:
        raise HTTPException(status_code=404, detail="Verification code not found")

    if datetime.utcnow() - verification_record.password_verified_at > timedelta(minutes=1):
        raise HTTPException(status_code=400, detail="Verification code has expired")

    if verify_new_password.code is None or not verification_record:
        raise HTTPException(status_code=400, detail="Code must be provided")

    if verify_new_password.code != verification_record.password_code:
        raise HTTPException(status_code=400, detail="Code does not match")

    existing_user.password = verify_new_password.new_password
    db.commit()
    return {"message": "Password has been changed successfully"}

