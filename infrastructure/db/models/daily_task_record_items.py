from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.db.database import Base

class DailyTaskRecordItemModel(Base):
    __tablename__ = "daily_task_record_items"

    __table_args__ = (
        UniqueConstraint("record_id", "user_id", "task_id", name="uq_record_task_once_per_day"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    record_id = Column(Integer, ForeignKey("daily_task_records.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    record = relationship("DailyTaskRecordModel", back_populates="items")   # ← class 名稱
    task = relationship("HabitModel", backref="daily_task_items")      # ← class 名稱