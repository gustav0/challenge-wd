import logging

from app.adapters.mocks import mock_sendgrid_api_call
from app.ports.email_service import EmailService

logger = logging.getLogger(__name__)


class SendGridService(EmailService):
    def __init__(self, api_key: str, from_email: str):
        self.api_key = api_key
        self.from_email = from_email

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> bool:
        # Actual SendGrid integration would go here
        logger.info(
            f"\n\n[SendGrid Email Service] Sending email to {to_email} with subject '{subject}' and body '{body}'\n"
        )
        response = await mock_sendgrid_api_call(to_email, subject, body)
        return response
