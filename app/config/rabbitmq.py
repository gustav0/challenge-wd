from typing import Optional

from pydantic_settings import BaseSettings

from app.config.utils import ConnectionURL


class RabbitMQConfig(BaseSettings):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    virtual_host: Optional[str] = "/"

    @property
    def url(self) -> str:
        url = ConnectionURL(
            "pyamqp",
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            path=self.virtual_host,
        )
        return url.as_string()
