from fastapi import APIRouter, Depends

from app.services.auth_service import AuthService
from dependencies import get_auth_service
from schemas.auth_schema import LoginRequest, RegisterRequest, UpdateUserResponse, UserResponse

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

@router.post("/update/{user_id}", response_model=UpdateUserResponse)
def update_user(
    user_id: int,
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return {
        "message": "User updated successfully",
        "data": auth_service.update_user(user_id, data.username, data.email, data.password)
    }