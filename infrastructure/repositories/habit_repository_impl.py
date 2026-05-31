from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import ProgrammingError, OperationalError
from datetime import date, timedelta

from infrastructure.db.models.habit_model import HabitModel
from infrastructure.db.models.habit_checkin_model import HabitCheckinModel
from domain.entities.habit import HabitEntity, CheckInEntity
from domain.repositories.habit_repository import HabitRepository


def _ensure_tables_exist():
    # import here to avoid circular imports at module import time
    from infrastructure.db.database import Base, engine

    Base.metadata.create_all(bind=engine)


class HabitRepositoryImpl(HabitRepository):
    def __init__(self, db: Session):
        self.db = db

    def _habit_period_start(self, frequency_type: str) -> date:
        today = date.today()
        frequency = (frequency_type or "").lower()

        if frequency == "weekly":
            return today - timedelta(days=today.weekday())
        if frequency == "monthly":
            return today.replace(day=1)
        return today

    def _is_habit_checked_in(self, habit_id: int, frequency_type: str) -> bool:
        period_start = self._habit_period_start(frequency_type)
        row = (
            self.db.query(HabitCheckinModel)
            .filter(HabitCheckinModel.habit_id == habit_id)
            .filter(HabitCheckinModel.date >= period_start)
            .filter(HabitCheckinModel.status == "completed")
            .first()
        )
        return row is not None

    def _decorate_habit(self, row: HabitModel) -> HabitEntity:
        habit = HabitEntity.from_orm(row)
        habit.is_checked_in = self._is_habit_checked_in(row.id, row.frequency_type)
        return habit

    def list_habits(self, user_id: int) -> List[HabitEntity]:
        rows = self.db.query(HabitModel).filter(HabitModel.user_id == user_id).all()
        return [self._decorate_habit(r) for r in rows]

    def create_habit(self, user_id: int, **data) -> HabitEntity:
        payload = {**data, "user_id": user_id}
        habit = HabitModel(**payload)
        try:
            self.db.add(habit)
            self.db.commit()
            self.db.refresh(habit)
            return self._decorate_habit(habit)
        except (ProgrammingError, OperationalError) as exc:
            # likely missing table; try to create tables then retry once
            self.db.rollback()
            _ensure_tables_exist()
            try:
                self.db.add(habit)
                self.db.commit()
                self.db.refresh(habit)
                return self._decorate_habit(habit)
            except Exception:
                self.db.rollback()
                raise

    def get_habit(self, habit_id: int, user_id: int = None):
        q = self.db.query(HabitModel).filter(HabitModel.id == habit_id)
        if user_id is not None:
            q = q.filter(HabitModel.user_id == user_id)
        row = q.first()
        if not row:
            return None
        return self._decorate_habit(row)

    def update_habit(self, habit_id: int, user_id: int = None, **data):
        q = self.db.query(HabitModel).filter(HabitModel.id == habit_id)
        if user_id is not None:
            q = q.filter(HabitModel.user_id == user_id)
        row = q.first()
        if not row:
            return None
        for k, v in data.items():
            setattr(row, k, v)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._decorate_habit(row)

    def delete_habit(self, habit_id: int, user_id: int = None) -> None:
        q = self.db.query(HabitModel).filter(HabitModel.id == habit_id)
        if user_id is not None:
            q = q.filter(HabitModel.user_id == user_id)
        row = q.first()
        if not row:
            return
        self.db.delete(row)
        self.db.commit()

    def create_checkin(self, habit_id: int, **data) -> CheckInEntity:
        payload = {**data, "habit_id": habit_id}
        checkin = HabitCheckinModel(**payload)
        try:
            self.db.add(checkin)
            self.db.commit()
            self.db.refresh(checkin)
            return CheckInEntity.from_orm(checkin)
        except (ProgrammingError, OperationalError):
            self.db.rollback()
            _ensure_tables_exist()
            try:
                self.db.add(checkin)
                self.db.commit()
                self.db.refresh(checkin)
                return CheckInEntity.from_orm(checkin)
            except Exception:
                self.db.rollback()
                raise

    def delete_checkins_for_period(self, habit_id: int) -> None:
        """Delete any 'completed' checkins for the habit within the current period.

        Current period follows the same logic as _is_habit_checked_in (daily/weekly/monthly).
        """
        # get habit to determine frequency_type
        habit = self.db.query(HabitModel).filter(HabitModel.id == habit_id).first()
        if not habit:
            return
        period_start = self._habit_period_start(habit.frequency_type)
        try:
            q = self.db.query(HabitCheckinModel)
            q = q.filter(HabitCheckinModel.habit_id == habit_id)
            q = q.filter(HabitCheckinModel.date >= period_start)
            q = q.filter(HabitCheckinModel.status == "completed")
            q.delete(synchronize_session=False)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def list_checkins(self, habit_id: int):
        rows = self.db.query(HabitCheckinModel).filter(HabitCheckinModel.habit_id == habit_id).all()
        return [CheckInEntity.from_orm(r) for r in rows]

    def list_checkins_for_month(self, month: str):
        """Aggregate checkins for the given month string 'YYYY-MM'. Returns dict with summary and days list."""
        import calendar as _calendar
        from datetime import datetime, date

        year, mon = month.split("-")
        year = int(year)
        mon = int(mon)
        _, last_day = _calendar.monthrange(year, mon)
        start_date = date(year, mon, 1)
        end_date = date(year, mon, last_day)

        rows = (
            self.db.query(HabitCheckinModel)
            .filter(HabitCheckinModel.date >= start_date)
            .filter(HabitCheckinModel.date <= end_date)
            .all()
        )

        # build per-day aggregation
        days_map = {}
        for r in rows:
            d = r.date.isoformat()
            if d not in days_map:
                days_map[d] = {"date": d, "completion_count": 0, "intensity": 0}
            # treat any completed as count; intensity as number of checkins
            if r.status == "completed":
                days_map[d]["completion_count"] += 1
            days_map[d]["intensity"] += 1

        days = list(days_map.values())
        total_days = last_day
        completed_days = len([1 for v in days if v["completion_count"] > 0])
        completion_rate = completed_days / total_days if total_days else 0.0

        return {
            "month": month,
            "summary": {
                "completed_days": completed_days,
                "total_days": total_days,
                "completion_rate": completion_rate,
            },
            "days": days,
        }

    def aggregate_stats(self):
        """Return simplified stats overview aggregation."""
        from datetime import date, timedelta

        today = date.today()
        seven_days_ago = today - timedelta(days=6)

        # trend 7 days
        trend_rows = (
            self.db.query(HabitCheckinModel)
            .filter(HabitCheckinModel.date >= seven_days_ago)
            .all()
        )

        trend_map = {}
        for i in range(7):
            d = (seven_days_ago + timedelta(days=i)).isoformat()
            trend_map[d] = 0

        for r in trend_rows:
            key = r.date.isoformat()
            if key in trend_map:
                if r.status == "completed":
                    trend_map[key] += 1

        trend_7_days = [{"date": k, "count": v} for k, v in trend_map.items()]

        # simple totals for today
        today_rows = (
            self.db.query(HabitCheckinModel)
            .filter(HabitCheckinModel.date == today)
            .all()
        )
        today_completed = len([r for r in today_rows if r.status == "completed"])
        today_total = len(today_rows)

        # completion rate across all recorded days
        all_rows = self.db.query(HabitCheckinModel).all()
        days_with_completion = set([r.date.isoformat() for r in all_rows if r.status == "completed"])
        unique_days = set([r.date.isoformat() for r in all_rows])
        completion_rate = (len(days_with_completion) / len(unique_days)) if unique_days else 0.0

        # streaks: naive calculation per habit current streak (approx)
        # For simplicity, compute max_streak as max consecutive completed days overall
        dates_completed = sorted(list(days_with_completion))
        max_streak = 0
        current_streak = 0
        prev_date = None
        from datetime import datetime as _dt
        for d in dates_completed:
            dt = _dt.fromisoformat(d).date()
            if prev_date and (dt - prev_date).days == 1:
                current_streak += 1
            else:
                current_streak = 1
            if current_streak > max_streak:
                max_streak = current_streak
            prev_date = dt

        return {
            "completion_rate": completion_rate,
            "today_completed": today_completed,
            "today_total": today_total,
            "average_streak": float(max_streak) if max_streak else 0.0,
            "max_streak": max_streak,
            "trend_7_days": trend_7_days,
            "streak_distribution": {"long_term": 0, "building": 0, "new": 0},
            "top_habits": [],
        }

    def profile_summary(self, user_id: int = None):
        """Return a minimal profile structure. Real implementation should join users and settings."""
        return {
            "user": {"id": "user_001", "display_name": "習慣實踐者", "email": "habit.user@example.com", "avatar_url": None},
            "summary": {"completion_rate": 0.0, "total_streak": 0, "best_habit": None},
            "settings": {"notifications_enabled": True, "theme": "dark", "timezone": "Asia/Taipei"},
        }
