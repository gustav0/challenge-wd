from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.preferences.database_adapter import DatabasePreferencesRepository
from app.ports.preferences_repository import PreferencesRepository


def get_preferences_repository(
    session: AsyncSession,
) -> PreferencesRepository:
    """
    This should return a repository adapter with a database session.
    The active adapter could change based on some configuration.
    """
    return DatabasePreferencesRepository(session=session)
