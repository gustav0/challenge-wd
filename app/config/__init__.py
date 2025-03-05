import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.database import DBSettings
from app.config.email_service import EmailServiceConfig
from app.config.internal_service import PropertiesServiceConfig, UserRepositoryConfig
from app.config.logging import LoggingConfig, setup_logging
from app.config.queue import QueueConfig
from app.config.sms_service import SMSServiceConfig


class Settings(BaseSettings):
    debug: bool = False
    app_name: str = "property-alerts"
    version: str = "0.0.1"
    port: int = 8000
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    database: DBSettings
    queue: QueueConfig
    logging: LoggingConfig

    property_service: PropertiesServiceConfig
    user_repository: UserRepositoryConfig

    email_service: EmailServiceConfig
    sms_service: SMSServiceConfig

    model_config = SettingsConfigDict(
        # Reading from .env file is the fastest way, but
        # ideally this would be in a secret store manager.
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


# variables are read from .env
settings = Settings()  # type: ignore[call-arg]
setup_logging(settings.logging)
