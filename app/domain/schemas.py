from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.infraestructure.db.models import (
    EmailNotificationDetail as EmailNotificationDetailTable,
)
from app.infraestructure.db.models import Preferences as PreferencesTable
from app.infraestructure.db.models import (
    SMSNotificationDetail as SMSNotificationDetailTable,
)

# These are an equivalent of DTOs


class User(BaseModel):
    id: str
    email: str
    phone_number: str


class Property(BaseModel):
    id: str
    address: str
    property_type: str
    price: float


class Preferences(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = False
    property_types: List[str] = []
    location: Optional[str] = None

    @classmethod
    def from_orm(cls, record: PreferencesTable) -> "Preferences":
        return cls(
            email_enabled=record.email_enabled,
            sms_enabled=record.sms_enabled,
            property_types=record.property_types,
            location=record.location,
        )


class EmailNotificationDetail(BaseModel):
    to_email: str
    subject: str
    html_body: str
    text_body: str
    from_email: Optional[str] = None


class SMSNotificationDetail(BaseModel):
    message: str
    to_phone_number: str
    from_phone_number: Optional[str]


class Notification(BaseModel):
    # Notifications might have different fields depending on the notification type.
    id: int
    user_id: str
    property_id: str
    notification_type: str
    scheduled_time_utc: datetime
    sent: Optional[bool] = None
    service_response: Optional[dict] = {}

    details: Optional[EmailNotificationDetail | SMSNotificationDetail] = None

    @classmethod
    def from_orm(
        cls, record: EmailNotificationDetailTable | SMSNotificationDetailTable
    ) -> "Notification":
        details: Optional[EmailNotificationDetail | SMSNotificationDetail] = None
        
        if isinstance(record, EmailNotificationDetailTable):
            details = EmailNotificationDetail(
                to_email=record.to_email,
                subject=record.subject,
                html_body=record.html_body,
                text_body=record.text_body,
                from_email=record.from_email,
            )
        elif isinstance(record, SMSNotificationDetailTable):
            details = SMSNotificationDetail(
                from_phone_number=record.from_phone_number,
                to_phone_number=record.to_phone_number,
                message=record.message,
            )

        return cls(
            id=record.id,
            user_id=record.user_id,
            property_id=record.property_id,
            notification_type=record.notification_type,
            scheduled_time_utc=record.scheduled_time_utc,
            service_response=record.service_response,
            sent=record.sent,
            details=details,
        )
