from abc import ABC, abstractmethod
from typing import Any


class EmailService(ABC):
    @abstractmethod
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> Any: ...
