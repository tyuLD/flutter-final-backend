from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, date


class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency_type: str
    reminder_time: Optional[str] = None
    minimum_action: Optional[str] = None
    identity_label: Optional[str] = None


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency_type: Optional[str] = None
    reminder_time: Optional[str] = None
    minimum_action: Optional[str] = None
    identity_label: Optional[str] = None
    is_active: Optional[bool] = None


class HabitRead(HabitBase):
    id: int
    is_checked_in: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class HabitCreateResponse(BaseModel):
    message: str
    data: HabitRead


class CheckInCreate(BaseModel):
    date: date
    status: str
    note: Optional[str] = None


class CheckInRead(BaseModel):
    id: int
    habit_id: int
    date: date
    status: str
    note: Optional[str] = None
    created_at: datetime


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


class ProfileResponse(BaseModel):
    user: Dict[str, Optional[str]]
    summary: Dict[str, Optional[float]]
    settings: Dict[str, Optional[str]]
