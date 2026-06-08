import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class CalendarRepository(ABC):
    @abstractmethod
    def get_daily_task_record(self, user_id: int, target_date: Optional[str] = None) -> List[Dict]:
        """List daily tasks for a given user and date (default to today)."""
        pass

    @abstractmethod
    def add_daily_task(self, user_id: int, task_id: int):
        pass

    @abstractmethod
    def count_total_daily_habits(self, user_id: int) -> int:
        pass

    @abstractmethod
    def list_daily_task_records_for_month(self, user_id: int, year: int, month: int) -> List[Dict]:
        pass
