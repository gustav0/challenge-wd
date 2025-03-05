import logging

from app.ports.sms_service import SMSService

logger = logging.getLogger(__name__)


class TwilioService(SMSService):
    def __init__(self, account_sid: str, auth_token: str, from_phone_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_phone_number = from_phone_number

    async def send_sms(self, to_phone_number: str, message: str) -> bool:
        # Actual Twilio integration would go here
        logger.info(
            f"\n\n[Twilio SMS Service] Sending SMS to {to_phone_number} with message '{message}'\n\n"
        )
        return True
