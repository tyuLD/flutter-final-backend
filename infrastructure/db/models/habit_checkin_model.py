from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.sql import func

from infrastructure.db.database import Base


class HabitCheckinModel(Base):
    __tablename__ = "habit_checkins"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(50), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
