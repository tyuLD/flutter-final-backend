from fastapi import APIRouter, Depends

from app.services.auth_service import AuthService
from dependencies import get_auth_service
from schemas.auth_schema import LoginRequest, RegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register(data.username, data.email, data.password)


@router.post("/login")
def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login(data.username, data.password)