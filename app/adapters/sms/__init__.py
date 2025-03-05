import logging

from app.adapters.sms.sns_adapter import SNSService
from app.adapters.sms.twilio_adapter import TwilioService
from app.config import settings
from app.ports.sms_service import SMSService

logger = logging.getLogger(__name__)
config = settings.sms_service

logger.info("Startup: Using email adapter %s", config.service)


def get_sms_service() -> SMSService:
    config = settings.sms_service

    # Considering we only have a couple of options an if statement is fine.
    if config.service == "twilio" and config.twilio is not None:
        return TwilioService(
            account_sid=config.twilio.account_sid,
            auth_token=config.twilio.auth_token,
            from_phone_number=config.twilio.from_phone_number,
        )
    elif config.service == "sns" and config.sns is not None:
        return SNSService(
            region=config.sns.region,
            access_key_id=config.sns.access_key_id,
            secret_access_key=config.sns.secret_access_key,
        )
    else:
        logger.error(
            f"Invalid SMS service type: {config.service} with config: {config}"
        )
        raise ValueError(
            f"Invalid SMS service type:{config.service} with config: {config}"
        )


sms_service = get_sms_service()
