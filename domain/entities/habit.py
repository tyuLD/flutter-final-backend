from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from dataclasses import dataclass, field


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


@dataclass
class DailyTaskRecordItemEntity:
    id: int
    record_id: int
    task_id: int
    completed_at: datetime

    @classmethod
    def from_orm(cls, obj) -> "DailyTaskRecordItemEntity":
        return cls(
            id=obj.id,
            record_id=obj.record_id,
            task_id=obj.task_id,
            completed_at=obj.completed_at,
        )

@dataclass
class DailyTaskRecordEntity:
    id: int
    day: date
    items: List[DailyTaskRecordItemEntity] = field(default_factory=list)

    @classmethod
    def from_orm(cls, obj) -> "DailyTaskRecordEntity":
        return cls(
            id=obj.id,
            day=obj.day,
            items=[DailyTaskRecordItemEntity.from_orm(i) for i in obj.items],
        )