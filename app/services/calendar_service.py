from datetime import date
from typing import Optional

from domain.repositories.calendar_repository import CalendarRepository


class CalendarService:
    def __init__(self, calendar_repository: CalendarRepository):
        self.calendar_repository = calendar_repository

    def _parse_date(self, value: Optional[str]) -> date:
        if value is None or value.strip() == "":
            return date.today()

        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format")

    def _build_daily_record_response(self, user_id: int, record):
        total_daily_habits = self.calendar_repository.count_total_daily_habits(user_id)
        completed_count = len(record.items)
        completion_rate = (
            completed_count / total_daily_habits if total_daily_habits > 0 else 0.0
        )

        return {
            "id": record.id,
            "day": record.day,
            "items": record.items,
            "completed_count": completed_count,
            "total_daily_habits": total_daily_habits,
            "completion_rate": completion_rate,
        }

    def get_daily_task_record(self, user_id: int, target_date: str):
        parsed_date = self._parse_date(target_date)
        record = self.calendar_repository.get_daily_task_record(user_id, parsed_date)
        return self._build_daily_record_response(user_id, record)

    def add_daily_task(
        self,
        user_id: int,
        task_id: int,
        target_date: Optional[str] = None,
    ):
        parsed_date = self._parse_date(target_date)
        return self.calendar_repository.add_daily_task(
            user_id=user_id,
            task_id=task_id,
            target_date=parsed_date,
        )

    def get_monthly_daily_records(self, user_id: int, month: str):
        try:
            year, mon = map(int, month.split("-"))
        except ValueError:
            raise ValueError("Month must be in YYYY-MM format")

        records = self.calendar_repository.list_daily_task_records_for_month(
            user_id=user_id,
            year=year,
            month=mon,
        )

        return {
            "month": month,
            "records": [
                self._build_daily_record_response(user_id, record)
                for record in records
            ],
        }