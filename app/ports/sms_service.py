from abc import ABC, abstractmethod
from typing import Any


class SMSService(ABC):
    @abstractmethod
    async def send_sms(
        self,
        to_phone_number: str,
        message: str,
    ) -> Any: ...
