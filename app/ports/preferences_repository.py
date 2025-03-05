from abc import ABC, abstractmethod
from typing import Optional

from app.domain.schemas import Preferences


class PreferencesRepository(ABC):
    @abstractmethod
    async def get_preferences_by_user_id(self, user_id: str) -> Optional[Preferences]:
        """Retrieve user preferences by user ID. May return None if not found"""
        ...

    @abstractmethod
    async def upsert_preferences(self, user_id: str, preferences: Preferences) -> int:
        """Update user preferences in the database. Returns updated rows"""
        ...
