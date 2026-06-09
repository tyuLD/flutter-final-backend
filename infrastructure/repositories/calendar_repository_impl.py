from datetime import date
from sqlalchemy.orm import Session, selectinload

from domain.repositories.calendar_repository import CalendarRepository
from infrastructure.db.models.daily_task_records import DailyTaskRecordModel
from infrastructure.db.models.daily_task_record_items import DailyTaskRecordItemModel
from infrastructure.db.models.habit_model import HabitModel


class CalendarRepositoryImpl(CalendarRepository):
    def __init__(self, db: Session):
        self.db = db

    def _get_or_create_record(self, user_id: int, target_date: date) -> DailyTaskRecordModel:
        record = (
            self.db.query(DailyTaskRecordModel)
            .options(selectinload(DailyTaskRecordModel.items))
            .filter(
                DailyTaskRecordModel.user_id == user_id,
                DailyTaskRecordModel.day == target_date,
            )
            .first()
        )

        if record:
            return record

        record = DailyTaskRecordModel(
            user_id=user_id,
            day=target_date,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return (
            self.db.query(DailyTaskRecordModel)
            .options(selectinload(DailyTaskRecordModel.items))
            .filter(DailyTaskRecordModel.id == record.id)
            .first()
        )

    def add_daily_task(self, user_id: int, task_id: int, target_date: date | None = None):
        target_date = target_date or date.today()
        record = self._get_or_create_record(user_id, target_date)

        existing = (
            self.db.query(DailyTaskRecordItemModel)
            .filter(
                DailyTaskRecordItemModel.record_id == record.id,
                DailyTaskRecordItemModel.user_id == user_id,
                DailyTaskRecordItemModel.task_id == task_id,
            )
            .first()
        )

        if existing:
            return existing

        item = DailyTaskRecordItemModel(
            user_id=user_id,
            record_id=record.id,
            task_id=task_id,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def remove_daily_task(
        self,
        user_id: int,
        task_id: int,
        target_date: date | None = None,
    ) -> bool:
        target_date = target_date or date.today()

        record = (
            self.db.query(DailyTaskRecordModel)
            .options(selectinload(DailyTaskRecordModel.items))
            .filter(
                DailyTaskRecordModel.user_id == user_id,
                DailyTaskRecordModel.day == target_date,
            )
            .first()
        )

        if not record:
            return False

        item = (
            self.db.query(DailyTaskRecordItemModel)
            .filter(
                DailyTaskRecordItemModel.record_id == record.id,
                DailyTaskRecordItemModel.user_id == user_id,
                DailyTaskRecordItemModel.task_id == task_id,
            )
            .first()
        )

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()

        remaining_count = (
            self.db.query(DailyTaskRecordItemModel)
            .filter(DailyTaskRecordItemModel.record_id == record.id)
            .count()
        )

        if remaining_count == 0:
            empty_record = (
                self.db.query(DailyTaskRecordModel)
                .filter(DailyTaskRecordModel.id == record.id)
                .first()
            )
            if empty_record:
                self.db.delete(empty_record)
                self.db.commit()

        return True

    def get_daily_task_record(self, user_id: int, target_date: date):
        return self._get_or_create_record(user_id, target_date)

    def count_total_daily_habits(self, user_id: int) -> int:
        return (
            self.db.query(HabitModel)
            .filter(
                HabitModel.user_id == user_id,
                HabitModel.frequency_type == "daily",
                HabitModel.is_active.is_(True),
            )
            .count()
        )

    def count_active_daily_habits(self, user_id: int) -> int:
        return self.count_total_daily_habits(user_id)

    def list_active_daily_habits(self, user_id: int):
        return (
            self.db.query(HabitModel)
            .filter(
                HabitModel.user_id == user_id,
                HabitModel.frequency_type == "daily",
                HabitModel.is_active.is_(True),
            )
            .all()
        )

    def list_daily_task_records_for_month(self, user_id: int, year: int, month: int):
        start_date = date(year, month, 1)
        end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

        return (
            self.db.query(DailyTaskRecordModel)
            .options(selectinload(DailyTaskRecordModel.items))
            .filter(DailyTaskRecordModel.user_id == user_id)
            .filter(DailyTaskRecordModel.day >= start_date)
            .filter(DailyTaskRecordModel.day < end_date)
            .order_by(DailyTaskRecordModel.day.asc())
            .all()
        )

    def list_daily_task_records_for_period(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ):
        return (
            self.db.query(DailyTaskRecordModel)
            .options(selectinload(DailyTaskRecordModel.items))
            .filter(DailyTaskRecordModel.user_id == user_id)
            .filter(DailyTaskRecordModel.day >= start_date)
            .filter(DailyTaskRecordModel.day <= end_date)
            .order_by(DailyTaskRecordModel.day.asc())
            .all()
        )