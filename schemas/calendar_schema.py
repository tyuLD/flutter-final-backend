from datetime import date, datetime
from typing import Dict, List, Optional

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


class CalendarDay(BaseModel):
    date: date
    completion_count: int
    intensity: int


class CalendarMonthResponse(BaseModel):
    month: str
    summary: Dict[str, Optional[float]]
    days: List[CalendarDay]


class StatsOverviewResponse(BaseModel):
    completion_rate: float
    today_completed: int
    today_total: int
    average_streak: float
    max_streak: int
    trend_7_days: List[Dict[str, int]]
    streak_distribution: Dict[str, int]
    top_habits: List[Dict[str, Optional[str]]]