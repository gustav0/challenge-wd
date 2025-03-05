import logging

from app.config import settings
from app.domain.exceptions import PreferencesNotFoundException, UserNotFoundException
from app.domain.schemas import Preferences
from app.ports.preferences_repository import PreferencesRepository
from app.ports.user_repository import UserRepository

logger = logging.getLogger(__name__)
config = settings.user_repository


class PreferencesService:
    """Use cases"""

    def __init__(
        self,
        preferences_repo: PreferencesRepository,
        user_repo: UserRepository,
    ):
        self.preferences_repo = preferences_repo
        self.user_repo = user_repo

    async def get_preferences(self, user_id: str) -> Preferences:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(
                f"PreferencesService/get_preferences: User {user_id} not found"
            )
        preferences = await self.preferences_repo.get_preferences_by_user_id(user_id)
        if not preferences:
            # This is technically the recommended way to interpolate strings in log messages,
            # although it's not the cleanest and performance gains are minimal in most cases.
            raise PreferencesNotFoundException(
                f"PreferencesService/get_preferences: Preferences not found for user {user_id}"
            )

        return preferences

    async def update_user_preferences(
        self,
        user_id: str,
        preferences: Preferences,
    ) -> Preferences:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(
                f"PreferencesService/update_preferences: User {user_id} not found"
            )

        updated = await self.preferences_repo.upsert_preferences(user_id, preferences)
        if not updated:
            raise PreferencesNotFoundException(
                f"PreferencesService/update_preferences: Failed to update preferences for user {user_id}"
            )

        return preferences
