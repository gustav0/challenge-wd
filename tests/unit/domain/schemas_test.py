from datetime import datetime, timezone

import pytest

from app.domain.schemas import Notification, Preferences
from app.infraestructure.db.models import EmailNotificationDetail
from app.infraestructure.db.models import Notification as NotificationTable
from app.infraestructure.db.models import Preferences as PreferencesTable


class TestPreferences:
    def test_from_orm(self):
        record = PreferencesTable(
            user_id=1,
            email_enabled=True,
            sms_enabled=False,
            property_types=["apartment", "house"],
            location="New York",
        )

        preferences = Preferences.from_orm(record)
        assert preferences.email_enabled is True
        assert preferences.sms_enabled is False
        assert preferences.property_types == ["apartment", "house"]
        assert preferences.location == "New York"


future_date: str = "2030-01-01T00:00:00.0Z"
data = [
    {
        "init": {
            "class": NotificationTable,
            "kwargs": {
                "id": 1,
                "user_id": "1",
                "property_id": "1",
                "notification_type": "email",
                "scheduled_time_utc": future_date,
                "sent": None,
            },
        },
        "expected": {
            "values": {
                "id": 1,
                "user_id": "1",
                "property_id": "1",
                "notification_type": "email",
                "scheduled_time_utc": future_date,
                "sent": None,
            },
            "details": None,
        },
    },
    {
        "init": {
            "class": EmailNotificationDetail,
            "kwargs": {
                "id": 1,
                "user_id": "1",
                "property_id": "1",
                "scheduled_time_utc": future_date,
                "sent": None,
                "service_response": None,
                "to_email": "to_email@email.com",
                "subject": "subject",
                "html_body": "html_body",
                "text_body": "text_body",
                "from_email": "from_email@email.com",
            },
        },
        "expected": {
            "values": {
                "id": 1,
                "user_id": "1",
                "property_id": "1",
                "scheduled_time_utc": future_date,
                "sent": None,
                "service_response": None,
                "notification_type": "email",
            },
            "details": {
                "to_email": "to_email@email.com",
                "subject": "subject",
                "html_body": "html_body",
                "text_body": "text_body",
                "from_email": "from_email@email.com",
            },
        },
    },
]


class TestNotification:
    @pytest.mark.parametrize("data", data)
    def test_from_orm(self, data):
        Class = data["init"]["class"]
        record = Class(**data["init"]["kwargs"])

        notification = Notification.from_orm(record)
        for key, value in data["expected"]["values"].items():
            if key == "scheduled_time_utc":
                # Parse date from string
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=timezone.utc
                )

            assert getattr(notification, key) == value

        if data["expected"]["details"]:
            for key, value in data["expected"]["details"].items():
                assert getattr(notification.details, key) == value
