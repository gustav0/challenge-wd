from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing_extensions import Literal


class TwilioConfig(BaseSettings):
    account_sid: str
    auth_token: str
    from_phone_number: str


class SNSConfig(BaseSettings):
    region: str
    access_key_id: str
    secret_access_key: str


class SMSServiceConfig(BaseSettings):
    service: Literal["twilio", "sns"]

    twilio: Optional[TwilioConfig] = None
    sns: Optional[SNSConfig] = None

    @model_validator(mode="after")
    def validate_service_config(self) -> "SMSServiceConfig":
        if getattr(self, self.service) is None:
            raise ValueError(
                f"SMS service is set to '{self.service}' but no config provided"
            )
        return self
