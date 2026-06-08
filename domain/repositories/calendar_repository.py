from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Dict, Any


class CalendarRepository(ABC):
    @abstractmethod
    def get_daily_task_record(self, user_id: int, target_date: date):
        pass

    @abstractmethod
    def add_daily_task(
        self,
        user_id: int,
        task_id: int,
        target_date: Optional[date] = None,
    ):
        pass

    @abstractmethod
    def count_total_daily_habits(self, user_id: int) -> int:
        pass

    @abstractmethod
    def list_daily_task_records_for_month(
        self,
        user_id: int,
        year: int,
        month: int,
    ) -> List:
        pass

    @abstractmethod
    def list_daily_task_records_for_period(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> List:
        pass

    @abstractmethod
    def list_active_daily_habits(self, user_id: int) -> List:
        pass

    @abstractmethod
    def count_active_daily_habits(self, user_id: int) -> int:
        pass