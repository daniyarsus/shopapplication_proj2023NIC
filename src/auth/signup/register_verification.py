from datetime import datetime
import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from src.settings.config import DOMAIN_NAME, API_KEY, SessionLocal, EMAIL_FROM, SMTP_PORT
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

    # Ищем существующий объект VerificationCode для пользователя или создаем новый
    verification_code = db.query(VerificationCode).filter(VerificationCode.user_id == existing_user.id).first()
    if verification_code:
        # Обновляем код и время, если запись найдена
        verification_code.email_code = code
        verification_code.email_verified_at = datetime.utcnow()
    else:
        # Создаем новую запись, если пользователь не найден
        verification_code = VerificationCode(
            user_id=existing_user.id,
            email_code=code,
            email_verified_at=datetime.utcnow()
        )
        db.add(verification_code)

    db.commit()

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    email = EMAIL_FROM
    receiver = post_email.email
    subject = "Отправка кода для регистрации"
    message = f"Ваш код: {str(code)}"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    server = smtplib.SMTP(DOMAIN_NAME, SMTP_PORT)
    server.starttls()
    server.login(email, API_KEY)
    server.send_message(msg)
    server.quit()

    return {"message": "Email sent successfully"}


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

