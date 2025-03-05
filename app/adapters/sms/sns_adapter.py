import logging

from app.ports.sms_service import SMSService

logger = logging.getLogger(__name__)


class SNSService(SMSService):
    def __init__(
        self,
        region: str,
        access_key_id: str,
        secret_access_key: str,
    ):
        self.region = region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    async def send_sms(self, to_phone_number: str, message: str) -> bool:
        # Actual AWS SNS integration would go here
        logger.info(
            f"\n\n[SNS SMS Service] Sending SMS to {to_phone_number} with message '{message}'\n\n"
        )
        return True
