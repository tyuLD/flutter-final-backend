from datetime import date
from typing import Optional

from domain.repositories.calendar_repository import CalendarRepository


class CalendarService:
    def __init__(self, repo: CalendarRepository):
        self.repo = repo

    def _parse_date(self, value: Optional[str]) -> date:
        if value is None or value.strip() == "":
            return date.today()

        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format")

    def get_daily_task_record(self, user_id: int, target_date: str):
        parsed_date = self._parse_date(target_date)
        return self.repo.get_daily_task_record(user_id=user_id, target_date=parsed_date)

    def add_daily_task(self, user_id: int, task_id: int, target_date: Optional[str] = None):
        parsed_date = self._parse_date(target_date)
        return self.repo.add_daily_task(
            user_id=user_id,
            task_id=task_id,
            target_date=parsed_date,
        )