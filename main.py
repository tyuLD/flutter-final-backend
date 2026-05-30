from fastapi import FastAPI

from infrastructure.db.database import Base, engine
from infrastructure.db.models.user_model import UserModel
from presentation.routers.auth_router import router as auth_router
from presentation.routers.habit_router import router as habit_router, calendar_router, stats_router, profile_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clean Architecture FastAPI")

app.include_router(auth_router)
app.include_router(habit_router)
app.include_router(calendar_router)
app.include_router(stats_router)
app.include_router(profile_router)


@app.get("/")
def root():
    return {"message": "server is running"}