from fastapi import HTTPException, status

from core.security import hash_password, verify_password
from domain.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, username: str, email: str, password: str):
        if self.user_repository.get_by_username(username):
            raise HTTPException(status_code=400, detail="username already exists")

        if self.user_repository.get_by_email(email):
            raise HTTPException(status_code=400, detail="email already exists")

        user = self.user_repository.create_user(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        }

    def login(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid username or password",
            )

        return {
            "user_id": user.id,
            "message": "login success",
            "username": user.username
        }
    
    def update_user(self, user_id: int, username: str, email: str, password: str):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if self.user_repository.get_by_username(username) and self.user_repository.get_by_username(username).id != user_id:
            raise HTTPException(status_code=400, detail="username already exists")

        if self.user_repository.get_by_email(email) and self.user_repository.get_by_email(email).id != user_id:
            raise HTTPException(status_code=400, detail="email already exists")

        updated_user = self.user_repository.update_user(
            user_id=user_id,
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )

        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "is_active": updated_user.is_active,
        }
    
    def get_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        }