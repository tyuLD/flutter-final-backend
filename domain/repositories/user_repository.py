from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def create_user(self, username: str, email: str, hashed_password: str) -> UserEntity:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass