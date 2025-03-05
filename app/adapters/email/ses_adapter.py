import logging

from app.adapters.mocks import mock_ses_api_call
from app.ports.email_service import EmailService

logger = logging.getLogger(__name__)


class SESService(EmailService):
    def __init__(
        self,
        region: str,
        access_key_id: str,
        secret_access_key: str,
        from_email: str,
    ):
        self.region = region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.from_email = from_email

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> bool:
        # Actual AWS SES integration would go here
        logger.info(
            f"\n\n[SES Email Service] Sending email to {to_email} with subject '{subject}' and body '{body}'\n\n"
        )
        result = await mock_ses_api_call(to_email, subject, body)
        return result
