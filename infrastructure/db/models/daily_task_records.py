from sqlalchemy import Column, Integer, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from infrastructure.db.database import Base

class DailyTaskRecordModel(Base):
    __tablename__ = "daily_task_records"

    __table_args__ = (
        UniqueConstraint("user_id", "day", name="uq_user_day_record"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    day = Column(Date, nullable=False, unique=True, index=True)

    items = relationship(
        "DailyTaskRecordItemModel",          # ← class 名稱
        back_populates="record",
        cascade="all, delete-orphan"
    )