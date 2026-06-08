from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class DailyTaskRecordItemResponse(BaseModel):
    id: int
    task_id: int
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompleteDailyTaskRequest(BaseModel):
    date: Optional[str] = None


class DailyTaskRecordResponse(BaseModel):
    id: int
    day: date
    items: List[DailyTaskRecordItemResponse] = Field(default_factory=list)
    completed_count: int
    total_daily_habits: int
    completion_rate: float

    model_config = ConfigDict(from_attributes=True)


class MonthlyDailyRecordResponse(BaseModel):
    month: str
    records: List[DailyTaskRecordResponse] = Field(default_factory=list)


class SevenDayDailyRecordResponse(BaseModel):
    start_date: date
    end_date: date
    records: List[DailyTaskRecordResponse] = Field(default_factory=list)


class OverviewHabitMetricResponse(BaseModel):
    habit_id: Optional[int] = None
    habit_name: Optional[str] = None
    completion_rate: float = 0.0
    completed_days: int = 0
    total_days: int = 0
    current_streak: int = 0


class OverviewSummaryResponse(BaseModel):
    completion_rate: float
    tracked_habits_count: int
    best_habit: Optional[OverviewHabitMetricResponse] = None
    needs_improvement_habit: Optional[OverviewHabitMetricResponse] = None


class StatsOverviewResponse(BaseModel):
    range_start: date
    range_end: date
    daily_records: List[DailyTaskRecordResponse] = Field(default_factory=list)
    summary: OverviewSummaryResponse