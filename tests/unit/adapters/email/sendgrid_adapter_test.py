import pytest

from app.adapters.email.sendgrid_adapter import SendGridService
from app.ports.email_service import EmailService

from . import sendgrid_adapter_data as data


class TestSendGridService:

    def test_valid_adapter(self):
        assert issubclass(SendGridService, EmailService)
        adapter = SendGridService(api_key="", from_email="")
        assert isinstance(adapter, EmailService)

    def test_init(self):
        api_key = "my_test_api_key"
        from_email = "from-email-2@example.com"
        adapter = SendGridService(api_key=api_key, from_email=from_email)

        assert adapter.api_key == api_key
        assert adapter.from_email == from_email

    @pytest.mark.parametrize(
        "data",
        data.test_send_email,
    )
    @pytest.mark.asyncio
    async def test_send_email(self, data, mocker):
        mock = mocker.patch(
            "app.adapters.email.sendgrid_adapter.mock_sendgrid_api_call",
            return_value=True,
        )
        adapter = SendGridService(
            api_key=data["init"]["api_key"],
            from_email=data["init"]["from_email"],
        )
        response = await adapter.send_email(
            to_email=data["init"]["to_email"],
            subject=data["init"]["subject"],
            body=data["init"]["body"],
        )

        assert response is True
        mock.assert_called_once_with(
            data["init"]["to_email"], data["init"]["subject"], data["init"]["body"]
        )
