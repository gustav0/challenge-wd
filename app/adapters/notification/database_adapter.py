import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import with_polymorphic

from app.domain.exceptions import NotificationNotFoundException
from app.domain.schemas import Notification
from app.infraestructure.db.models import (
    EmailNotificationDetail as EmailNotificationDetailTable,
)
from app.infraestructure.db.models import Notification as NotificationTable
from app.infraestructure.db.models import (
    SMSNotificationDetail as SMSNotificationDetailTable,
)
from app.ports.notifications_repository import NotificationRepository

logger = logging.getLogger(__name__)


class DatabaseNotificationRepository(NotificationRepository):
    def __init__(self, session: AsyncSession):
        """
        Initialize the repository adapter with a database session.
        """
        self.session = session

    async def get_notification_by_id(
        self, notification_id: int
    ) -> Optional[Notification]:
        """
        Fetch a single notification by its ID.
        """
        stmt = select(with_polymorphic(NotificationTable, "*")).where(
            NotificationTable.id == notification_id
        )
        result = await self.session.execute(stmt)

        record = result.scalars().one_or_none()

        if not record:
            return None

        return Notification.from_orm(record)  # type: ignore[arg-type]

    async def insert_email_notification(
        self,
        user_id: str,
        property_id: str,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        scheduled_time_utc: datetime,
        from_email: Optional[str] = None,
        sent: Optional[bool] = None,
        service_response: Optional[dict] = None,
    ) -> Notification:
        email_notification = EmailNotificationDetailTable(
            user_id=user_id,
            property_id=property_id,
            notification_type="email",
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            scheduled_time_utc=scheduled_time_utc.replace(tzinfo=None),
            from_email=from_email,
            sent=sent,
            service_response=service_response,
        )

        self.session.add(email_notification)
        await self.session.commit()
        await self.session.refresh(email_notification)
        return Notification.from_orm(email_notification)

    async def insert_sms_notification(
        self,
        user_id: str,
        property_id: str,
        to_phone_number: str,
        message: str,
        scheduled_time_utc: datetime,
        from_phone_number: Optional[str] = None,
        sent: Optional[bool] = None,
        service_response: Optional[dict] = None,
    ) -> Notification:
        sms_notification = SMSNotificationDetailTable(
            user_id=user_id,
            property_id=property_id,
            to_phone_number=to_phone_number,
            message=message,
            scheduled_time_utc=scheduled_time_utc.replace(tzinfo=None),
            from_phone_number=from_phone_number,
            sent=sent,
            service_response=service_response,
        )

        self.session.add(sms_notification)
        await self.session.commit()
        await self.session.refresh(sms_notification)
        return Notification.from_orm(sms_notification)

    async def update_notification_status(
        self, notification_id: int, sent: bool, service_response: dict
    ) -> Notification:
        """
        Update a notification's sent status and service response.
        """
        stmt = (
            update(NotificationTable)
            .where(NotificationTable.id == notification_id)
            .values(sent=sent, service_response=service_response)
            .returning(NotificationTable.id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()

        updated_id = result.scalar_one_or_none()
        if not updated_id:
            logger.error(
                f"Notification with id {notification_id} not found during update"
            )
            raise NotificationNotFoundException(
                f"Notification with id {notification_id} not found during update"
            )

        notification = await self.get_notification_by_id(updated_id)
        if not notification:
            raise NotificationNotFoundException(
                f"Notification with id {notification_id} not found during update"
            )
        return notification
