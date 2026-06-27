from fastapi import FastAPI

from infrastructure.db.database import Base, engine
from infrastructure.db.models.user_model import UserModel
from infrastructure.db.models.habit_model import HabitModel
from infrastructure.db.models.daily_task_records import DailyTaskRecordModel
from infrastructure.db.models.daily_task_record_items import DailyTaskRecordItemModel
from infrastructure.db.models.habit_checkin_model import HabitCheckinModel
from infrastructure.db.models.daily_habit_list_model import DailyHabitListModel
from presentation.routers.auth_router import router as auth_router,profile_router
from presentation.routers.habit_router import router as habit_router, stats_router
from presentation.routers.calendar_router import router as calendar_router
from presentation.routers.keep_router import router as keep_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clean Architecture FastAPI")

app.include_router(auth_router)
app.include_router(habit_router)
app.include_router(calendar_router)
app.include_router(stats_router)
app.include_router(profile_router)
app.include_router(keep_router)


@app.get("/")
def root():
    return {"message": "server is running"}