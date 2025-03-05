import asyncio
import logging

from app.domain.schemas import User
from app.infraestructure.celery import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def dispatch_notification_task(self, notification_id: int, user: dict):
    from app.domain.services.notification_service import NotificationService

    logger.info(
        "sending_notification_task %s with id %s for user %s",
        self,
        notification_id,
        user,
    )

    User(**user)  # Check if the user is valid

    # There might be safer ways to do this, like async_to_sync
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        NotificationService.trigger_notification(notification_id, user)
    )
