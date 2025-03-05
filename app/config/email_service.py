from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing_extensions import Literal


class SendGridConfig(BaseSettings):
    api_key: str
    from_email: str


class SESConfig(BaseSettings):
    region: str
    access_key_id: str
    secret_access_key: str
    from_email: str


class EmailServiceConfig(BaseSettings):
    service: Literal["sendgrid", "ses"]

    # The following are only required if service specifies them. Achieved by the `validate_service_config` validator.
    sendgrid: Optional[SendGridConfig] = None
    ses: Optional[SESConfig] = None

    @model_validator(mode="after")
    def validate_service_config(self) -> "EmailServiceConfig":
        if getattr(self, self.service) is None:
            raise ValueError(
                f"Email service is set to '{self.service}' but no config provided"
            )
        return self
