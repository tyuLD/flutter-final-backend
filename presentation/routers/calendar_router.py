from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.calendar_service import CalendarService
from dependencies import get_calendar_service
from schemas.calendar_schema import (
    CompleteDailyTaskRequest,
    DailyTaskRecordItemResponse,
    DailyTaskRecordResponse,
    MonthlyDailyRecordResponse,
    StatsOverviewResponse,
)

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.post("/day", response_model=DailyTaskRecordItemResponse)
def add_daily_task(
    body: CompleteDailyTaskRequest,
    task_id: int = Query(..., description="Task ID"),
    user_id: int = Query(..., description="User ID"),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    try:
        return calendar_service.add_daily_task(
            user_id=user_id,
            task_id=task_id,
            target_date=body.date,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/day", response_model=DailyTaskRecordResponse)
def get_daily_task_record(
    user_id: int = Query(..., description="User ID"),
    date: str | None = Query(None, description="Target date (YYYY-MM-DD)"),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    try:
        return calendar_service.get_daily_task_record(
            user_id=user_id,
            target_date=date,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/month", response_model=MonthlyDailyRecordResponse)
def get_monthly_daily_records(
    user_id: int = Query(..., description="User ID"),
    month: str = Query(..., description="Month in YYYY-MM format"),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    try:
        return calendar_service.get_monthly_daily_records(
            user_id=user_id,
            month=month,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/week", response_model=StatsOverviewResponse)
def get_stats_overview(
    user_id: int = Query(..., description="User ID"),
    end_date: str | None = Query(
        None,
        description="End date in YYYY-MM-DD format, default is today",
    ),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    try:
        return calendar_service.get_stats_overview(
            user_id=user_id,
            end_date_value=end_date,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))