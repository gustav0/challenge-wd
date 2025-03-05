from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.domain.schemas import Notification


class NotificationRepository(ABC):
    @abstractmethod
    async def get_notification_by_id(
        self, notification_id: int
    ) -> Optional[Notification]:
        """
        Fetch a single notification by its ID.
        """
        ...

    @abstractmethod
    async def update_notification_status(
        self, notification_id: int, sent: bool, service_response: dict
    ) -> Notification:
        """
        Update the notification's sent status and service response.
        """
        ...

    @abstractmethod
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
        """
        Insert a new email notification into the database and return the created notification."""
        ...

    @abstractmethod
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
        """
        Insert a new SMS notification into the database and return the created notification."""
        ...
