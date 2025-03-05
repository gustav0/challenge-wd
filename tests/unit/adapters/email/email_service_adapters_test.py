from unittest.mock import MagicMock

import pytest

from app.adapters.email import get_email_service
from app.adapters.email.sendgrid_adapter import SendGridService
from app.adapters.email.ses_adapter import SESService


class TestGetEmailService:
    @pytest.fixture
    def mock_config(self, mocker):
        return mocker.patch("app.adapters.email.config")

    def test_get_email_service_sendgrid(self, mock_config):
        # Mock the SendGrid config
        mock_config.service = "sendgrid"
        mock_config.sendgrid = MagicMock(
            api_key="test_api_key", from_email="test@sendgrid.com"
        )

        email_service = get_email_service()

        assert isinstance(email_service, SendGridService)
        assert email_service.api_key == "test_api_key"
        assert email_service.from_email == "test@sendgrid.com"

    def test_get_email_service_ses(self, mock_config):
        # Mock the SES config
        mock_config.service = "ses"
        mock_config.ses = MagicMock(
            region="aws_region",
            access_key_id="test_access_key",
            secret_access_key="test_secret_key",
            from_email="test@ses.com",
        )

        email_service = get_email_service()

        assert isinstance(email_service, SESService)
        assert email_service.region == "aws_region"
        assert email_service.access_key_id == "test_access_key"
        assert email_service.secret_access_key == "test_secret_key"
        assert email_service.from_email == "test@ses.com"

    def test_get_email_service_invalid_service(self, mock_config):
        # Invalid service configuration
        mock_config.service = "unknown"
        mock_config.sendgrid = None
        mock_config.ses = None

        with pytest.raises(ValueError, match="Invalid email service type: unknown"):
            get_email_service()

    @pytest.mark.parametrize("service", ["sendgrid", "ses"])
    def test_get_email_service_missing_config(self, mock_config, service):
        # Valid service but missing configuration
        mock_config.service = service
        setattr(mock_config, service, None)

        with pytest.raises(
            ValueError,
            match=f"Invalid email service type: {service} with config",
        ):
            get_email_service()
