import pytest

from app.adapters.email.ses_adapter import SESService
from app.ports.email_service import EmailService

from . import ses_adapter_data as data


class TestSESService:

    def test_valid_adapter(self):
        assert issubclass(SESService, EmailService)

        adapter = SESService(
            region="",
            access_key_id="",
            secret_access_key="",
            from_email="",
        )
        assert isinstance(adapter, EmailService)

    def test_init(self):
        region = "aws-region"
        access_key_id = "my-test-access-key-id"
        secret_access_key = "my-test-secret-access-key"
        from_email = "from-email@example.com"
        adapter = SESService(
            region=region,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            from_email=from_email,
        )

        assert adapter.region == region
        assert adapter.access_key_id == access_key_id
        assert adapter.secret_access_key == secret_access_key
        assert adapter.from_email == from_email

    @pytest.mark.parametrize(
        "data",
        data.test_send_email,
    )
    @pytest.mark.asyncio
    async def test_send_email(self, data, mocker):
        mock = mocker.patch(
            "app.adapters.email.ses_adapter.mock_ses_api_call",
            return_value=True,
        )
        adapter = SESService(
            region=data["init"]["region"],
            access_key_id=data["init"]["access_key_id"],
            secret_access_key=data["init"]["secret_access_key"],
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
