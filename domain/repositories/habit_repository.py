from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.habit import HabitEntity, CheckInEntity


class HabitRepository(ABC):
    @abstractmethod
    def list_habits(self, user_id: int) -> List[HabitEntity]:
        pass

    @abstractmethod
    def create_habit(self, user_id: int, **data) -> HabitEntity:
        pass

    @abstractmethod
    def get_habit(self, habit_id: int, user_id: int) -> Optional[HabitEntity]:
        pass

    @abstractmethod
    def update_habit(self, habit_id: int, user_id: int, **data) -> Optional[HabitEntity]:
        pass

    @abstractmethod
    def delete_habit(self, habit_id: int, user_id: int) -> None:
        pass


    @abstractmethod
    def create_checkin(self, habit_id: int, **data) -> CheckInEntity:
        pass

    @abstractmethod
    def delete_checkins_for_period(self, habit_id: int) -> None:
        """Delete completed checkins for the current habit period (used for checkout/undo)."""
        pass

    @abstractmethod
    def list_checkins(self, habit_id: int):
        pass

    @abstractmethod
    def list_checkins_for_month(self, month: str):
        """Return aggregated checkin data for a given month string 'YYYY-MM'."""
        pass

    @abstractmethod
    def aggregate_stats(self):
        """Return aggregated statistics used by stats overview."""
        pass

    @abstractmethod
    def profile_summary(self, user_id: int = None):
        """Return profile summary and settings for a user (user_id optional)."""
        pass
