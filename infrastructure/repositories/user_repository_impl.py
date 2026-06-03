from sqlalchemy.orm import Session

from infrastructure.db.models.user_model import UserModel
from domain.entities.user import UserEntity
from domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            return None
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )

    def get_by_email(self, email: str):
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )

    def create_user(self, username: str, email: str, hashed_password: str):
        user = UserModel(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )
    
    def get_by_id(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )
    
    def update_user(self, user_id: int, username: str, email: str, hashed_password: str):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        
        user.username = username
        user.email = email
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)

        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )