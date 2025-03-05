from abc import ABC, abstractmethod
from typing import Optional

from app.domain.schemas import User


class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(
        self,
        id: str,
    ) -> Optional[User]:
        """Fetch user from the UserRepository (different microservice)"""
        ...
