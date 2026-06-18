from datetime import date

from fastapi import HTTPException, status

from core.security import hash_password, verify_password
from domain.repositories.user_repository import UserRepository
from domain.repositories.habit_repository import HabitRepository
from domain.repositories.calendar_repository import CalendarRepository


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        habit_repository: HabitRepository,
        calendar_repository: CalendarRepository,
    ):
        self.user_repository = user_repository
        self.habit_repository = habit_repository
        self.calendar_repository = calendar_repository

    def register(self, username: str, email: str, password: str):
        if self.user_repository.get_by_username(username):
            raise HTTPException(status_code=400, detail="username already exists")

        if self.user_repository.get_by_email(email):
            raise HTTPException(status_code=400, detail="email already exists")

        user = self.user_repository.create_user(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )

        self._bootstrap_new_user(user.id)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        }

    def _bootstrap_new_user(self, user_id: int):
        default_habits = [
            {
                "name": "喝水",
                "description": "每天至少喝一杯水",
                "frequency_type": "daily",
                "is_active": True,
            },
            {
                "name": "閱讀 10 分鐘",
                "description": "每天固定閱讀 10 分鐘",
                "frequency_type": "daily",
                "is_active": True,
            },
            {
                "name": "早睡",
                "description": "每天提早休息",
                "frequency_type": "daily",
                "is_active": True,
            },
        ]

        for habit_data in default_habits:
            self.habit_repository.create_habit(user_id, **habit_data)

        self.calendar_repository.get_daily_task_record(
            user_id=user_id,
            target_date=date.today(),
        )

    def login(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid username or password",
            )

        return {
            "user_id": user.id,
            "message": "login success",
            "username": user.username,
        }

    def update_user(self, user_id: int, username: str, email: str, password: str):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        existing_username_user = self.user_repository.get_by_username(username)
        if existing_username_user and existing_username_user.id != user_id:
            raise HTTPException(status_code=400, detail="username already exists")

        existing_email_user = self.user_repository.get_by_email(email)
        if existing_email_user and existing_email_user.id != user_id:
            raise HTTPException(status_code=400, detail="email already exists")

        updated_user = self.user_repository.update_user(
            user_id=user_id,
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )

        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "is_active": updated_user.is_active,
        }

    def get_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        }