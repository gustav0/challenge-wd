from typing import Literal, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings

from app.config.rabbitmq import RabbitMQConfig
from app.config.redis import RedisConfig


class CeleryConfig(BaseSettings):
    broker: Literal["redis", "rabbitmq"]

    redis: Optional[RedisConfig] = None
    rabbitmq: Optional[RabbitMQConfig] = None

    # COMMENT: This is also a valid approach, providing the Connection URL
    # directly instead of the service config. Using both approaches is not
    # a great idea though, we should stick to one.
    result_backend: str

    task_serializer: Optional[str] = "json"
    accept_content: Optional[list[str]] = ["json"]
    timezone: Optional[str] = "UTC"

    @property
    def broker_url(self) -> str:
        return getattr(self, self.broker).url

    @model_validator(mode="after")
    def validate_engine_config(self) -> "CeleryConfig":
        if getattr(self, self.broker) is None:
            raise ValueError(
                f"Celery broker is set to '{self.broker}' but no config provided"
            )
        return self


class QueueConfig(BaseSettings):
    service: Literal["celery", "fastapi", "custom"]

    celery: Optional[CeleryConfig] = None

    @model_validator(mode="after")
    def validate_service_config(self) -> "QueueConfig":

        if self.service == "fastapi":
            # FastAPI BackgroundTasks requires no additional config
            return self

        if self.service == "custom":
            # We might need/want to implement a custom queue system
            raise ValueError("Custom queue service is not supported yet")

        if getattr(self, self.service) is None:
            raise ValueError(f"Queue is set to '{self.service}' but no config provided")
        return self
