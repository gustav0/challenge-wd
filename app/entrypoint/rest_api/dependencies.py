"""
FastAPI dependencies
"""

# If this ends up growing, we can split it up into multiple files.
from typing import AsyncGenerator

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.email import get_email_service as _get_email_service
from app.adapters.notification import (
    get_notifications_repository as _get_notifications_repository,
)
from app.adapters.preferences import (
    get_preferences_repository as _get_preferences_repository,
)
from app.adapters.property import get_property_service
from app.adapters.queue import get_queue_adapter as _get_queue_adapter
from app.adapters.sms import get_sms_service as _get_sms_service
from app.adapters.user import get_user_repository as _get_user_repository
from app.domain.services.notification_service import NotificationService
from app.domain.services.preferences_service import PreferencesService
from app.infraestructure.db.database import Session
from app.ports.email_service import EmailService
from app.ports.notifications_repository import NotificationRepository
from app.ports.preferences_repository import PreferencesRepository
from app.ports.property_service import PropertyService
from app.ports.queue_port import QueuePort
from app.ports.sms_service import SMSService
from app.ports.user_repository import UserRepository


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide a database session.
    Using it guarantees only one session is open at a time per request.
    Guarantees that the session is closed after the request.
    """
    async with Session() as session:
        yield session


async def get_preferences_repository(
    session: AsyncSession = Depends(get_db_session),
) -> PreferencesRepository:
    """
    Dependency to provide the PreferencesRepository, with a database session.
    """
    return _get_preferences_repository(session=session)


async def get_notifications_repository(
    session: AsyncSession = Depends(get_db_session),
) -> NotificationRepository:
    """
    Dependency to provide the PreferencesRepository, with a database session.
    """
    return _get_notifications_repository(session=session)


async def get_email_service() -> EmailService:
    """
    This is 'useless' overhead at the moment, but there might be
    a need to update the email service later. I.e override some stuff
    when ran from FastAPI vs CLI.
    """
    return _get_email_service()


async def get_sms_service() -> SMSService:
    return _get_sms_service()


async def get_user_repository() -> UserRepository:
    return _get_user_repository()


async def get_queue_adapter(background_tasks: BackgroundTasks) -> QueuePort:
    return _get_queue_adapter(background_tasks=background_tasks)


async def get_notifications_service(
    notifications_repo: NotificationRepository = Depends(get_notifications_repository),
    preferences_repo: PreferencesRepository = Depends(get_preferences_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    sms_service: SMSService = Depends(get_sms_service),
    email_service: EmailService = Depends(get_email_service),
    property_service: PropertyService = Depends(get_property_service),
    queue: QueuePort = Depends(get_queue_adapter),
) -> NotificationService:
    return NotificationService(
        notifications_repo,
        sms_service,
        email_service,
        preferences_repo,
        user_repo,
        property_service,
        queue,
    )


async def get_preferences_service(
    preferences_repo: PreferencesRepository = Depends(get_preferences_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> PreferencesService:
    return PreferencesService(preferences_repo, user_repo)


__all__ = [
    "get_db_session",
    "get_preferences_repository",
    "get_notifications_repository",
    "get_email_service",
    "get_sms_service",
    "get_user_repository",
]
