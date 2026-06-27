from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/health", tags=["Health Check"])

@router.get("/check", summary="Health Check Endpoint", description="Returns the health status of the API service.")
def health_check():
    return {
        "status": "ok",
        "service": "habit-flow-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }