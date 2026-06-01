from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class HabitEntity(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    frequency_type: str
    reminder_time: Optional[str] = None
    minimum_action: Optional[str] = None
    identity_label: Optional[str] = None
    is_checked_in: bool = False
    current_streak: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CheckInEntity(BaseModel):
    id: int
    habit_id: int
    date: date
    status: str
    note: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
