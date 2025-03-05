from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from pydantic import BaseModel, field_validator


class NotificationResponse(BaseModel):
    id: int
    user_id: str
    property_id: str
    notification_type: str
    scheduled_time_utc: datetime
    sent: Optional[bool] = None
    service_response: Optional[dict] = {}

    details: Mapping[str, Any]


class ScheduleNotificationInput(BaseModel):
    user_id: str
    message: str
    property_id: str
    scheduled_time_utc: datetime

    @field_validator("scheduled_time_utc", mode="after")
    def validate_scheduled_time_utc(cls, value: datetime):
        if value <= datetime.now(timezone.utc):
            raise ValueError("Scheduled time must be in the future")
        return value


class ScheduleNotificationResponse(BaseModel):
    notification_ids: list[int]
