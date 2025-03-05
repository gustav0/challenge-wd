from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.notification.database_adapter import DatabaseNotificationRepository
from app.ports.notifications_repository import NotificationRepository


def get_notifications_repository(
    session: AsyncSession,
) -> NotificationRepository:
    """
    This should return a notifications repository adapter with a database session.
    The active adapter could change based on some configuration.
    """
    return DatabaseNotificationRepository(session=session)
