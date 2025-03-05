import logging
from datetime import datetime

from app.adapters.email import get_email_service
from app.adapters.notification import get_notifications_repository
from app.adapters.preferences import get_preferences_repository
from app.adapters.property import get_property_service
from app.adapters.queue import get_queue_adapter
from app.adapters.sms import get_sms_service
from app.adapters.user import get_user_repository
from app.domain.exceptions import (
    NotificationDispatchException,
    NotificationNotFoundException,
    PreferencesNotFoundException,
    PropertyNotFoundException,
    UserNotFoundException,
)
from app.domain.schemas import (
    EmailNotificationDetail,
    Notification,
    SMSNotificationDetail,
    User,
)
from app.infraestructure.db.database import Session
from app.ports.email_service import EmailService
from app.ports.notifications_repository import NotificationRepository
from app.ports.preferences_repository import PreferencesRepository
from app.ports.property_service import PropertyService
from app.ports.queue_port import QueuePort
from app.ports.sms_service import SMSService
from app.ports.user_repository import UserRepository

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        notifications_repo: NotificationRepository,
        sms_sender: SMSService,
        email_sender: EmailService,
        preferences_repo: PreferencesRepository,
        user_repo: UserRepository,
        property_service: PropertyService,
        queue: QueuePort,
    ):
        """
        Initialize the service with a repository port.
        """
        self.notifications_repo = notifications_repo
        self.preferences_repo = preferences_repo
        self.sms_sender = sms_sender
        self.email_sender = email_sender
        self.user_repo = user_repo
        self.property_service = property_service
        self.queue = queue

    async def get_notification_by_id(self, notification_id: int) -> Notification:
        """
        Fetch a single notification by ID.
        """
        notification = await self.notifications_repo.get_notification_by_id(
            notification_id
        )
        if notification is None:
            raise NotificationNotFoundException(
                f"Notification with ID {notification_id} not found"
            )
        return notification

    async def schedule_notification(
        self,
        user_id: str,
        property_id: str,
        message: str,
        scheduled_time_utc: datetime,
    ) -> list[int]:
        """
        Send a notification and update its status in the database.
        """

        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        preferenses = await self.preferences_repo.get_preferences_by_user_id(user_id)
        if not preferenses:
            raise PreferencesNotFoundException(
                f"User preferences not found for user ID {user_id}"
            )

        property = await self.property_service.get_property_by_id(property_id)
        if not property:
            raise PropertyNotFoundException(f"Property with ID {property_id} not found")

        generated_notification_ids = []
        if preferenses.email_enabled:
            email_notification = await self.notifications_repo.insert_email_notification(
                user_id=user_id,
                property_id=property_id,
                to_email=user.email,
                subject="New Property Notification",  # Marketing team should change this subject
                text_body=message,
                html_body=message,  # This needs some work. It should be HTML Template. NotificationTemplate system maybe?
                scheduled_time_utc=scheduled_time_utc,
            )
            generated_notification_ids.append(email_notification.id)

        if preferenses.sms_enabled:
            sms_notification = await self.notifications_repo.insert_sms_notification(
                user_id=user_id,
                property_id=property_id,
                to_phone_number=user.phone_number,
                message=message,
                scheduled_time_utc=scheduled_time_utc,
            )

            generated_notification_ids.append(sms_notification.id)

        for notification_id in generated_notification_ids:
            await self.queue.schedule_task(
                task=self.dispatch_notification,
                notification_id=notification_id,
                user=user.model_dump(),
                # This is not supported by FastAPI Bckground Tasks adapter
                # but could be implemented with Celery or other Queue Adapters
                eta=scheduled_time_utc,
            )

        return generated_notification_ids

    async def dispatch_notification(self, notification_id: int, user: dict) -> None:
        """
        Sends a notification and updates its status in the database.
        """
        notification = await self.get_notification_by_id(notification_id)

        cleaned_user = User(**user)

        if notification.notification_type == "email":
            if isinstance(notification.details, EmailNotificationDetail):
                response = await self.email_sender.send_email(
                    to_email=cleaned_user.email,
                    body=notification.details.html_body,
                    subject="Property Alert",  # Yea this should be a Notification's property
                )
            else:
                raise NotificationDispatchException(
                    f"Invalid email notification details from notification {notification_id}"
                )
        elif notification.notification_type == "sms":
            if isinstance(notification.details, SMSNotificationDetail):
                response = await self.sms_sender.send_sms(
                    message=notification.details.message,
                    to_phone_number=cleaned_user.phone_number,
                )
            else:
                raise NotificationDispatchException(
                    f"Invalid sms notification details from notification {notification_id}"
                )

        if response and not isinstance(response, dict):
            response = {"details": str(response)}

        await self.notifications_repo.update_notification_status(
            notification_id=notification_id,
            sent=True,
            service_response=response,
        )

    @classmethod
    async def trigger_notification(cls, notification_id: int, user: dict) -> None:
        """
        Utility class level wrapper to trigger a notification.

        Streamlines the process of sending a notification, specially from Queue adapters
        """
        async with Session() as session:
            notifications_repo = get_notifications_repository(session=session)
            sms_sender = get_sms_service()
            email_sender = get_email_service()
            preferences_repo = get_preferences_repository(session=session)
            user_repo = get_user_repository()
            property_service = get_property_service()
            queue = get_queue_adapter()

            service = cls(
                notifications_repo=notifications_repo,
                sms_sender=sms_sender,
                email_sender=email_sender,
                preferences_repo=preferences_repo,
                user_repo=user_repo,
                property_service=property_service,
                queue=queue,
            )

            await service.dispatch_notification(
                notification_id=notification_id, user=user
            )
