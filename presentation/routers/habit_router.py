from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from schemas.habit_schema import (
    HabitCreate,
    HabitCreateResponse,
    HabitRead,
    HabitUpdate,
    CheckInCreate,
    CheckInRead,
    CalendarMonthResponse,
    StatsOverviewResponse,
    ProfileResponse,
)
from app.services.habit_service import HabitService
from dependencies import get_habit_service


router = APIRouter(prefix="/habits", tags=["Habits"])


@router.get("", response_model=List[HabitRead])
def list_habits(user_id: int = Query(..., description="User ID to list habits for"), habit_service: HabitService = Depends(get_habit_service)):
    return habit_service.list_habits(user_id)


@router.post("", response_model=HabitCreateResponse)
def create_habit(user_id: int = Query(..., description="User ID that owns the habit"), data: HabitCreate = None, habit_service: HabitService = Depends(get_habit_service)):
    try:
        habit = habit_service.create_habit(user_id, data)
        return {"message": "Habit created successfully", "data": habit}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create habit")


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, user_id: int = Query(..., description="User ID"), habit_service: HabitService = Depends(get_habit_service)):
    item = habit_service.get_habit(habit_id, user_id=user_id)
    if not item:
        raise HTTPException(status_code=404, detail="Habit not found")
    return item


@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: int, user_id: int = Query(..., description="User ID"), data: HabitUpdate = None, habit_service: HabitService = Depends(get_habit_service)):
    item = habit_service.update_habit(habit_id, user_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Habit not found")
    return item


@router.delete("/{habit_id}")
def delete_habit(habit_id: int, user_id: int = Query(..., description="User ID"), habit_service: HabitService = Depends(get_habit_service)):
    habit_service.delete_habit(habit_id, user_id)
    return {"ok": True}


@router.post("/{habit_id}/checkins", response_model=CheckInRead)
def create_checkin(habit_id: int, user_id: int = Query(..., description="User ID"), data: CheckInCreate = None, habit_service: HabitService = Depends(get_habit_service)):
    try:
        return habit_service.create_checkin(habit_id, user_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Habit not found or not owned by user")


@router.post("/{habit_id}/checkouts")
def create_checkout(habit_id: int, user_id: int = Query(..., description="User ID"), habit_service: HabitService = Depends(get_habit_service)):
    try:
        habit_service.checkout(habit_id, user_id)
        return {"ok": True}
    except ValueError:
        raise HTTPException(status_code=404, detail="Habit not found or not owned by user")


@router.get("/{habit_id}/checkins", response_model=List[CheckInRead])
def list_checkins(habit_id: int, user_id: int = Query(..., description="User ID"), habit_service: HabitService = Depends(get_habit_service)):
    try:
        return habit_service.list_checkins(habit_id, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Habit not found or not owned by user")


# 下面為建議的獨立路由，可按需註冊到 app
calendar_router = APIRouter(prefix="/calendar", tags=["Calendar"]) 


@calendar_router.get("/overview", response_model=CalendarMonthResponse)
def calendar_overview(month: str = Query(..., description="YYYY-MM"), user_id: int = Query(None, description="User ID (optional)"), habit_service: HabitService = Depends(get_habit_service)):
    # current implementation aggregates across all users; later can scope by user_id
    return habit_service.calendar_overview(month)


stats_router = APIRouter(prefix="/stats", tags=["Stats"]) 


@stats_router.get("/overview", response_model=StatsOverviewResponse)
def stats_overview(user_id: int = Query(None, description="User ID (optional)"), habit_service: HabitService = Depends(get_habit_service)):
    # current implementation aggregates across all users; later can scope by user_id
    return habit_service.stats_overview()


profile_router = APIRouter(prefix="/profile", tags=["Profile"]) 


@profile_router.get("/me", response_model=ProfileResponse)
def profile_me(user_id: int = Query(None, description="User ID (optional)"), habit_service: HabitService = Depends(get_habit_service)):
    return habit_service.profile_me()
