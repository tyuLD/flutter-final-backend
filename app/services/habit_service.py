from typing import List, Optional
from domain.repositories.habit_repository import HabitRepository
from domain.repositories.calendar_repository import CalendarRepository
from domain.entities.habit import HabitEntity, CheckInEntity
from datetime import date

from schemas.habit_schema import (
    HabitCreate,
    HabitUpdate,
    CheckInCreate,
)


class HabitService:
    def __init__(self,
        habit_repo: HabitRepository,
        calendar_repo: CalendarRepository,
    ):
        self.habit_repo = habit_repo
        self.calendar_repo = calendar_repo

    def list_habits(self, user_id: int) -> List[HabitEntity]:
        return self.habit_repo.list_habits(user_id)

    def create_habit(self, user_id: int, data: HabitCreate) -> HabitEntity:
        payload = data.dict()
        return self.habit_repo.create_habit(user_id, **payload)

    def get_habit(self, habit_id: int, user_id: int = None) -> Optional[HabitEntity]:
        return self.habit_repo.get_habit(habit_id, user_id=user_id)

    def update_habit(self, habit_id: int, user_id: int, data: HabitUpdate) -> Optional[HabitEntity]:
        payload = {k: v for k, v in data.dict().items() if v is not None}
        return self.habit_repo.update_habit(habit_id, user_id=user_id, **payload)

    def delete_habit(self, habit_id: int, user_id: int) -> None:
        return self.habit_repo.delete_habit(habit_id, user_id=user_id)

    def create_checkin(self, habit_id: int, user_id: int, data: CheckInCreate) -> CheckInEntity:
        print("[HabitService] create_checkin start", habit_id, user_id)

        habit = self.get_habit(habit_id, user_id=user_id)
        if not habit:
            raise ValueError("Habit not found or not owned by user")

        payload = data.dict()
        payload.setdefault("status", "completed")
        print("[HabitService] payload =", payload)

        checkin = self.habit_repo.create_checkin(habit_id, user_id, **payload)
        print("[HabitService] habit checkin created", checkin)

        result = self.calendar_repo.add_daily_task(
            user_id=user_id,
            task_id=habit_id,
            target_date=checkin.date,
        )
        print("[HabitService] calendar result =", result)

        return checkin

    def checkout(self, habit_id: int, user_id: int) -> None:
        habit = self.get_habit(habit_id, user_id=user_id)
        if not habit:
            raise ValueError("Habit not found or not owned by user")

        self.habit_repo.delete_checkins_for_period(habit_id)
        target_date = date.today()

        self.calendar_repo.remove_daily_task(
            user_id=user_id,
            task_id=habit_id,
            target_date=target_date,
        )

        return None

    def list_checkins(self, habit_id: int, user_id: int) -> List[CheckInEntity]:
        habit = self.get_habit(habit_id, user_id=user_id)
        if not habit:
            raise ValueError("Habit not found or not owned by user")
        return self.habit_repo.list_checkins(habit_id)
    
    # Simple stubs for calendar/stats/profile: real implementations should aggregate from repo
    def calendar_overview(self, month: str):
        return self.habit_repo.list_checkins_for_month(month)

    def stats_overview(self):
        return self.habit_repo.aggregate_stats()

    def profile_me(self):
        return self.habit_repo.profile_summary()
