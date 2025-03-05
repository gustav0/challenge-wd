import logging

from app.adapters.email.sendgrid_adapter import SendGridService
from app.adapters.email.ses_adapter import SESService
from app.config import settings
from app.ports.email_service import EmailService

logger = logging.getLogger(__name__)
config = settings.email_service

logger.info("Startup: Using email adapter %s", config.service)


def get_email_service() -> EmailService:
    # Considering we only have a couple of options an if statement is fine.
    if config.service == "sendgrid" and config.sendgrid is not None:
        return SendGridService(
            api_key=config.sendgrid.api_key,
            from_email=config.sendgrid.from_email,
        )
    elif config.service == "ses" and config.ses is not None:
        return SESService(
            region=config.ses.region,
            access_key_id=config.ses.access_key_id,
            secret_access_key=config.ses.secret_access_key,
            from_email=config.ses.from_email,
        )
    else:
        logger.error(
            f"Invalid email service type: {config.service} with config: {config}"
        )
        raise ValueError(
            f"Invalid email service type: {config.service} with config: {config}"
        )


email_service = get_email_service()

__all__ = [
    "email_service",
    "get_email_service",
]
