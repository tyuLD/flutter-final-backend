from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional, List, Dict
from datetime import datetime, date


class HabitBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: Optional[str] = None
    frequency_type: str = Field(validation_alias=AliasChoices("frequencyType", "frequency_type"))
    reminder_time: Optional[str] = Field(default=None, validation_alias=AliasChoices("reminderTime", "reminder_time"))
    minimum_action: Optional[str] = Field(default=None, validation_alias=AliasChoices("minimumAction", "minimum_action"))
    identity_label: Optional[str] = Field(default=None, validation_alias=AliasChoices("identityLabel", "identity_label"))


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = None
    description: Optional[str] = None
    frequency_type: Optional[str] = Field(default=None, validation_alias=AliasChoices("frequencyType", "frequency_type"))
    reminder_time: Optional[str] = Field(default=None, validation_alias=AliasChoices("reminderTime", "reminder_time"))
    minimum_action: Optional[str] = Field(default=None, validation_alias=AliasChoices("minimumAction", "minimum_action"))
    identity_label: Optional[str] = Field(default=None, validation_alias=AliasChoices("identityLabel", "identity_label"))
    is_active: Optional[bool] = Field(default=None, validation_alias=AliasChoices("isActive", "is_active"))


class HabitRead(HabitBase):
    id: int
    is_checked_in: bool = Field(default=False)
    current_streak: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime
    updated_at: datetime


class HabitCreateResponse(BaseModel):
    message: str
    data: HabitRead


class CheckInCreate(BaseModel):
    date: date
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
