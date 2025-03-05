import pytest

from app.domain.exceptions import NotificationNotFoundException
from app.domain.schemas import Preferences
from app.domain.services.notification_service import NotificationService
from app.ports.email_service import EmailService
from app.ports.notifications_repository import NotificationRepository
from app.ports.preferences_repository import PreferencesRepository
from app.ports.property_service import PropertyService
from app.ports.queue_port import QueuePort
from app.ports.sms_service import SMSService
from app.ports.user_repository import UserRepository

from . import notification_service_data as data


class TestNotificationService:
    @pytest.fixture
    def mock_notification_repo(self, mocker):
        return mocker.AsyncMock(spec=NotificationRepository)

    @pytest.fixture
    def mock_sms_sender(self, mocker):
        return mocker.Mock(spec=SMSService)

    @pytest.fixture
    def mock_email_sender(self, mocker):
        return mocker.Mock(spec=EmailService)

    @pytest.fixture
    def mock_preferences_repo(self, mocker):
        return mocker.Mock(spec=PreferencesRepository)

    @pytest.fixture
    def mock_user_repository(self, mocker):
        return mocker.AsyncMock(spec=UserRepository)

    @pytest.fixture
    def mock_property_service(self, mocker):
        return mocker.Mock(spec=PropertyService)

    @pytest.fixture
    def mock_queue(self, mocker):
        return mocker.Mock(spec=QueuePort)

    def test_initialize(
        self,
        mock_notification_repo,
        mock_sms_sender,
        mock_email_sender,
        mock_preferences_repo,
        mock_user_repository,
        mock_property_service,
        mock_queue,
    ):
        notification_service = NotificationService(
            notifications_repo=mock_notification_repo,
            sms_sender=mock_sms_sender,
            email_sender=mock_email_sender,
            preferences_repo=mock_preferences_repo,
            user_repo=mock_user_repository,
            property_service=mock_property_service,
            queue=mock_queue,
        )

        assert notification_service.notifications_repo == mock_notification_repo
        assert notification_service.sms_sender == mock_sms_sender
        assert notification_service.email_sender == mock_email_sender
        assert notification_service.preferences_repo == mock_preferences_repo
        assert notification_service.user_repo == mock_user_repository
        assert notification_service.property_service == mock_property_service
        assert notification_service.queue == mock_queue

    @pytest.mark.asyncio
    async def test_get_notification_by_id(self, mocker, mock_notification_repo):
        notification_service = NotificationService(
            notifications_repo=mock_notification_repo,
            sms_sender=mocker.Mock(),
            email_sender=mocker.Mock(),
            preferences_repo=mocker.Mock(),
            user_repo=mocker.Mock(),
            property_service=mocker.Mock(),
            queue=mocker.Mock(),
        )
        notification_id = 1
        notification = mocker.Mock()

        mock_notification_repo.get_notification_by_id.return_value = notification
        result = await notification_service.get_notification_by_id(notification_id)

        mock_notification_repo.get_notification_by_id.assert_called_once_with(
            notification_id
        )

        assert result == notification

    @pytest.mark.asyncio
    async def test_get_notification_by_id_raises_exception(
        self,
        mocker,
        mock_notification_repo,
    ):
        notification_service = NotificationService(
            notifications_repo=mock_notification_repo,
            sms_sender=mocker.Mock(),
            email_sender=mocker.Mock(),
            preferences_repo=mocker.Mock(),
            user_repo=mocker.Mock(),
            property_service=mocker.Mock(),
            queue=mocker.Mock(),
        )
        notification_id = 1

        mock_notification_repo.get_notification_by_id.return_value = None

        with pytest.raises(NotificationNotFoundException):
            await notification_service.get_notification_by_id(notification_id)

    @pytest.mark.asyncio
    async def test_schedule_notification(
        self,
        mocker,
        mock_notification_repo,
        mock_sms_sender,
        mock_email_sender,
        mock_preferences_repo,
        mock_user_repository,
        mock_property_service,
        mock_queue,
    ):
        user_id = "1"
        phone_number = "1234567890"
        user_dump = {
            "id": user_id,
            "email": "test@test.com",
            "phone_number": phone_number,
        }
        user = mocker.Mock()
        user.model_dump.return_value = user_dump
        user.phone_number = phone_number
        mock_user_repository.get_user_by_id.return_value = user

        preferences = mocker.Mock(spec=Preferences)
        preferences.email_enabled = True
        preferences.sms_enabled = True
        mock_preferences_repo.get_preferences_by_user_id.return_value = preferences

        property_id = "1"
        property = mocker.Mock()
        mock_property_service.get_property_by_id.return_value = property

        sms_notification = mocker.Mock()
        sms_notification.id = 1
        email_notification = mocker.Mock()
        email_notification.id = 2
        mock_notification_repo.insert_sms_notification.return_value = sms_notification
        mock_notification_repo.insert_email_notification.return_value = (
            email_notification
        )

        message = mocker.Mock(spec=str)
        schedule_time = mocker.Mock()

        notification_service = NotificationService(
            notifications_repo=mock_notification_repo,
            sms_sender=mock_sms_sender,
            email_sender=mock_email_sender,
            preferences_repo=mock_preferences_repo,
            user_repo=mock_user_repository,
            property_service=mock_property_service,
            queue=mock_queue,
        )

        notification_ids = await notification_service.schedule_notification(
            user_id=user_id,
            property_id=property_id,
            message=message,
            scheduled_time_utc=schedule_time,
        )

        assert notification_ids == [2, 1]

        mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
        mock_preferences_repo.get_preferences_by_user_id.assert_called_once_with(
            user_id
        )
        mock_property_service.get_property_by_id.assert_called_once_with(property_id)

        mock_notification_repo.insert_sms_notification.assert_called_once_with(
            user_id=user_id,
            property_id=property_id,
            message=message,
            scheduled_time_utc=schedule_time,
            to_phone_number=phone_number,
        )

        mock_notification_repo.insert_email_notification.assert_called_once_with(
            user_id=user_id,
            property_id=property_id,
            text_body=message,
            html_body=message,
            scheduled_time_utc=schedule_time,
            to_email=user.email,
            subject="New Property Notification",
        )

        mock_queue.schedule_task.call_count == 2

        mock_queue.schedule_task.assert_called_with(
            task=notification_service.dispatch_notification,
            notification_id=sms_notification.id,
            user=user_dump,
            eta=schedule_time,
        )

    @pytest.mark.parametrize("data", data.test_get_notification_by_id_raises_exception)
    @pytest.mark.asyncio
    async def test_schedule_notification_raises_exception(
        self,
        data,
        mocker,
        mock_notification_repo,
        mock_sms_sender,
        mock_email_sender,
        mock_preferences_repo,
        mock_user_repository,
        mock_property_service,
        mock_queue,
    ):
        notification_service = NotificationService(
            notifications_repo=mock_notification_repo,
            sms_sender=mock_sms_sender,
            email_sender=mock_email_sender,
            preferences_repo=mock_preferences_repo,
            user_repo=mock_user_repository,
            property_service=mock_property_service,
            queue=mock_queue,
        )

        mock_user_repository.get_user_by_id.return_value = data["mock"][
            "get_user_by_id"
        ]
        mock_preferences_repo.get_preferences_by_user_id.return_value = data["mock"][
            "get_preferences_by_user_id"
        ]
        mock_property_service.get_property_by_id.return_value = data["mock"][
            "get_property_by_id"
        ]

        message = "Hey test!"
        schedule_time = mocker.Mock()

        with pytest.raises(data["expected_exception"]):
            await notification_service.schedule_notification(
                user_id="1",
                property_id="1",
                message=message,
                scheduled_time_utc=schedule_time,
            )
