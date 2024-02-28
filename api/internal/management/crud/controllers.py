from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.auth.models import User
from api.internal.management.models import Employee


class EmployeeManager:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.current_user = current_user

    async def create_employee(self, create_data):
        employee = Employee()


