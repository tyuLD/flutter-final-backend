from typing import List, Optional
from domain.repositories.habit_repository import HabitRepository
from domain.entities.habit import HabitEntity, CheckInEntity
from schemas.habit_schema import (
    HabitCreate,
    HabitUpdate,
    CheckInCreate,
)


class HabitService:
    def __init__(self, repo: HabitRepository):
        self.repo = repo

    def list_habits(self, user_id: int) -> List[HabitEntity]:
        return self.repo.list_habits(user_id)

    def create_habit(self, user_id: int, data: HabitCreate) -> HabitEntity:
        payload = data.dict()
        return self.repo.create_habit(user_id, **payload)

    def get_habit(self, habit_id: int, user_id: int = None) -> Optional[HabitEntity]:
        return self.repo.get_habit(habit_id, user_id=user_id)

    def update_habit(self, habit_id: int, user_id: int, data: HabitUpdate) -> Optional[HabitEntity]:
        payload = {k: v for k, v in data.dict().items() if v is not None}
        return self.repo.update_habit(habit_id, user_id=user_id, **payload)

    def delete_habit(self, habit_id: int, user_id: int) -> None:
        return self.repo.delete_habit(habit_id, user_id=user_id)

    def create_checkin(self, habit_id: int, user_id: int, data: CheckInCreate) -> CheckInEntity:
        # verify habit belongs to user
        habit = self.get_habit(habit_id, user_id=user_id)
        if not habit:
            raise ValueError("Habit not found or not owned by user")
        payload = data.dict()
        # default status to 'completed' for check-in
        payload.setdefault("status", "completed")
        return self.repo.create_checkin(habit_id, **payload)

    def checkout(self, habit_id: int, user_id: int) -> None:
        # verify habit belongs to user
        habit = self.get_habit(habit_id, user_id=user_id)
        if not habit:
            raise ValueError("Habit not found or not owned by user")
        return self.repo.delete_checkins_for_period(habit_id)

    def list_checkins(self, habit_id: int, user_id: int) -> List[CheckInEntity]:
        habit = self.get_habit(habit_id, user_id=user_id)
        if not habit:
            raise ValueError("Habit not found or not owned by user")
        return self.repo.list_checkins(habit_id)
    
    def complete_daily_task(self, user_id: int, task_id: int, target_date: Optional[str] = None):
        # This is a stub implementation. Real implementation should check if task belongs to user and is valid for the day.
        return self.repo.complete_daily_task(user_id, task_id, target_date=target_date)
    
    def daily_task_record(self, user_id: int, target_date: Optional[str] = None):
        # This is a stub implementation. Real implementation should return the record for the given day.
        return self.repo.get_daily_task_record(user_id, target_date=target_date)

    # Simple stubs for calendar/stats/profile: real implementations should aggregate from repo
    def calendar_overview(self, month: str):
        return self.repo.list_checkins_for_month(month)

    def stats_overview(self):
        return self.repo.aggregate_stats()

    def profile_me(self):
        return self.repo.profile_summary()
