from random import randint

from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.services.auth.models import User, VerificationCode
from api.services.auth.crud.signup.schemas import SignupEmailSend, SignupEmailVerify
from api.services.auth.crud.signup.schemas import SignupSchema
from api.settings.config import settings


class SignupManager:
    def __init__(self, form_data: SignupSchema, db: AsyncSession):
        self.form_data = form_data
        self.db = db

    async def _check_existing_user(self):
        query = select(User).where(User.username == self.form_data.username)
        existing_user = await self.db.execute(query)
        if existing_user:
            raise HTTPException(status_code=400, detail="User is registered")

    async def register_user(self):

        user = User(
            name=self.form_data.name,
            lastname=self.form_data.lastname,
            email=self.form_data.email,
            phone=self.form_data.phone,
            username=self.form_data.username,
            password=self.form_data.password
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return {"message": "Successfully registered"}


class EmailCodeManager:
    def __init__(self, post_email: SignupEmailSend, db: AsyncSession) -> None:
        self.post_email = post_email
        self.db = db

    async def send_email(self):
        try:
            db_user = await self._get_existing_user()
            await self._check_user_verification(db_user)

            code = generate_verification_code()

            verification_code = await self._get_or_create_verification_code(db_user, code)

            email = EMAIL_FROM
            receiver = self.post_email.email
            subject = "Отправка кода для регистрации"
            message = f"Ваш код: {str(code)}"

            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain', 'utf-8'))

            server = smtplib.SMTP(settings.smtp_gmail.DOMAIN_NAME, settings.smtp_gmail.SMTP_PORT)
            server.starttls()
            server.login(email, settings.smtp_gmail.API_KEY)
            server.send_message(msg)
            server.quit()

            return {"message": "Email sent successfully"}

        except HTTPException as e:
            raise e

    async def verify_code(self):
        try:
            db_user = await self._get_existing_user()

            verification_record = await self._get_latest_verification_code(db_user)

            await self._check_verification_code_expiry(verification_record)

            await self._check_verification_code_match(verification_record)

            db_user.is_verified = True
            await self.db.commit()

            return {"message": "User has been verified"}

        except HTTPException as e:
            raise e

    def generate_verification_code(self):
        try:
            code = randint(1000000, 9999999)
            return code
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def _get_existing_user(self):
        query = select(User).where(User.email == self.post_email.email)
        existing_user = await self.db.execute(query)
        db_user = existing_user.scalar_one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        return db_user

    async def _check_user_verification(self, db_user):
        if db_user.is_verified:
            raise HTTPException(status_code=400, detail="Email already verified")

    async def _get_or_create_verification_code(self, db_user, code):
        verification_code = await self.db.execute(
            select(VerificationCode).where(VerificationCode.user_id == db_user.id)
        )
        verification_code = verification_code.scalar_one_or_none()

        if verification_code:
            verification_code.email_code = code
            verification_code.email_verified_at = datetime.utcnow()
        else:
            verification_code = VerificationCode(
                user_id=db_user.id,
                email_code=code,
                email_verified_at=datetime.utcnow()
            )
            self.db.add(verification_code)

        await self.db.commit()

        return verification_code

    async def _get_latest_verification_code(self, db_user):
        verification_record = await self.db.execute(
            select(VerificationCode)
            .where(VerificationCode.user_id == db_user.id)
            .order_by(VerificationCode.email_verified_at.desc())
        )
        verification_record = verification_record.scalar_one_or_none()

        if not verification_record:
            raise HTTPException(status_code=404, detail="Verification code not found")

        return verification_record

    async def _check_verification_code_expiry(self, verification_record):
        if datetime.utcnow() - verification_record.email_verified_at > timedelta(minutes=1):
            raise HTTPException(status_code=400, detail="Verification code has expired")

    async def _check_verification_code_match(self, verification_record):
        if self.post_email.code is None or not verification_record:
            raise HTTPException(status_code=400, detail="Code must be provided")
        if self.post_email.code != verification_record.email_code:
            raise HTTPException(status_code=400, detail="Code does not match")
