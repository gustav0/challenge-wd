import datetime
from typing import Any, Optional

from sqlalchemy import Enum, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.config import settings

# COMMENT: Models could live in their own modules.
# But they are quite simple, so I decided to keep them together.

# It would be nice to have an AuditLog table.


class Base(AsyncAttrs, DeclarativeBase):
    __table_args__ = {
        "schema": (
            settings.database.db_schema
            if hasattr(settings.database, "db_schema")
            else None
        )
    }
    metadata = MetaData(
        schema=(
            settings.database.db_schema
            if hasattr(settings.database, "db_schema")
            else None
        )
    )
    type_annotation_map = {dict[str, Any]: JSONB, list[str]: JSONB}

    id: Mapped[int] = mapped_column(primary_key=True)


class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str]
    property_id: Mapped[str]
    scheduled_time_utc: Mapped[datetime.datetime]
    sent: Mapped[Optional[bool]] = mapped_column(default=None, nullable=True)
    service_response: Mapped[dict[str, Any]] = mapped_column(default={})
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), nullable=False
    )
    notification_type: Mapped[str] = mapped_column(
        Enum("email", "sms", name="notification_type_enum"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_on": "notification_type",
        "polymorphic_identity": "notificaton",
    }


class EmailNotificationDetail(Notification):
    __tablename__ = "email_notification_detail"

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("notification.id"),
        primary_key=True,
    )
    subject: Mapped[str]
    html_body: Mapped[str]
    text_body: Mapped[str]
    from_email: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    to_email: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "email",
    }


class SMSNotificationDetail(Notification):
    __tablename__ = "sms_notification_detail"

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("notification.id"),
        primary_key=True,
    )
    to_phone_number: Mapped[str]
    from_phone_number: Mapped[Optional[str]] = mapped_column(
        default=None, nullable=True
    )
    message: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "sms",
    }


class Preferences(Base):
    __tablename__ = "preferences"

    user_id: Mapped[str] = mapped_column(unique=True)
    email_enabled: Mapped[bool] = mapped_column(default=True)
    sms_enabled: Mapped[bool] = mapped_column(default=False)
    property_types: Mapped[list[str]] = mapped_column(
        default=[]
    )  # This should be a M2M relation
    location: Mapped[str] = mapped_column(default=None)

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )


__all__ = [
    "Base",
    "Notification",
]
