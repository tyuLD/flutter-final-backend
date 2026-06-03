from sqlalchemy import Column, Integer, Date, DateTime, JSON, UniqueConstraint
from sqlalchemy.sql import func

from infrastructure.db.database import Base


class DailyHabitListModel(Base):
    __tablename__ = "daily_habit_lists"
    __table_args__ = (
        UniqueConstraint("date", name="uq_daily_habit_lists_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    habit_ids = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())