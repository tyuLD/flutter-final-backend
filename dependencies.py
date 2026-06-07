from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from infrastructure.db.database import get_db
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl


def get_auth_service(db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    return AuthService(user_repository)


def get_habit_service(db: Session = Depends(get_db)):
    from infrastructure.repositories.habit_repository_impl import HabitRepositoryImpl
    from infrastructure.repositories.calendar_repository_impl import CalendarRepositoryImpl
    from app.services.habit_service import HabitService

    habit_repository = HabitRepositoryImpl(db)
    calendar_repository = CalendarRepositoryImpl(db)

    return HabitService(habit_repository, calendar_repository)


def get_calendar_repository(db: Session = Depends(get_db)):
    """獨立提供 CalendarRepository，方便 service 或測試直接注入。"""
    from infrastructure.repositories.calendar_repository_impl import CalendarRepositoryImpl

    return CalendarRepositoryImpl(db)


def get_calendar_service(db: Session = Depends(get_db)):
    """延遲 import，避免 calendar service / repository 尚未完成時循環匯入。"""
    from infrastructure.repositories.calendar_repository_impl import CalendarRepositoryImpl
    from app.services.calendar_service import CalendarService

    calendar_repository = CalendarRepositoryImpl(db)
    return CalendarService(calendar_repository)
