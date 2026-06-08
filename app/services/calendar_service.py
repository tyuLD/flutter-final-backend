from datetime import date, timedelta
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
        completion_rate = completed_count / total_daily_habits if total_daily_habits > 0 else 0.0

        return {
            "id": record.id,
            "day": record.day,
            "items": record.items,
            "completed_count": completed_count,
            "total_daily_habits": total_daily_habits,
            "completion_rate": completion_rate,
        }

    def get_daily_task_record(self, user_id: int, target_date: Optional[str] = None):
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

    def get_stats_overview(
        self,
        user_id: int,
        end_date_value: Optional[str] = None,
    ):
        end_date = self._parse_date(end_date_value)
        start_date = end_date - timedelta(days=6)

        records = self.calendar_repository.list_daily_task_records_for_period(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )
        active_habits = self.calendar_repository.list_active_daily_habits(user_id)
        total_daily_habits = self.calendar_repository.count_total_daily_habits(user_id)

        record_by_day = {record.day: record for record in records}

        daily_records = []
        total_completed = 0
        total_possible = total_daily_habits * 7

        for i in range(7):
            current_day = start_date + timedelta(days=i)
            record = record_by_day.get(current_day)

            if record is None:
                daily_records.append({
                    "id": 0,
                    "day": current_day,
                    "items": [],
                    "completed_count": 0,
                    "total_daily_habits": total_daily_habits,
                    "completion_rate": 0.0,
                })
                continue

            row = self._build_daily_record_response(user_id, record)
            total_completed += row["completed_count"]
            daily_records.append(row)

        overall_completion_rate = (
            total_completed / total_possible if total_possible > 0 else 0.0
        )

        habit_stats = []
        for habit in active_habits:
            completed_days = 0

            for record in records:
                task_ids = {item.task_id for item in record.items}
                if habit.id in task_ids:
                    completed_days += 1

            completion_rate = completed_days / 7 if 7 > 0 else 0.0

            habit_stats.append({
                "habit_id": habit.id,
                "habit_name": habit.name,
                "completion_rate": completion_rate,
                "completed_days": completed_days,
                "total_days": 7,
                "current_streak": 0,
            })

        best_habit = max(
            habit_stats,
            key=lambda x: (x["completion_rate"], x["completed_days"]),
            default=None,
        )

        needs_improvement_habit = min(
            habit_stats,
            key=lambda x: (x["completion_rate"], x["completed_days"]),
            default=None,
        )

        return {
            "range_start": start_date,
            "range_end": end_date,
            "daily_records": daily_records,
            "summary": {
                "completion_rate": overall_completion_rate,
                "tracked_habits_count": len(active_habits),
                "best_habit": best_habit,
                "needs_improvement_habit": needs_improvement_habit,
            },
        }