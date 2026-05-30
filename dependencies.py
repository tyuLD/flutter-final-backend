from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from infrastructure.db.database import get_db
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl


def get_auth_service(db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    return AuthService(user_repository)


def get_habit_service(db: Session = Depends(get_db)):
    """延遲 import 以避免在尚未實作 repository/service 時造成匯入錯誤。"""
    from infrastructure.repositories.habit_repository_impl import HabitRepositoryImpl
    from app.services.habit_service import HabitService

    habit_repository = HabitRepositoryImpl(db)
    return HabitService(habit_repository)