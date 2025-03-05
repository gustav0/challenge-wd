from typing import Optional

from pydantic_settings import BaseSettings

from app.config.utils import ConnectionURL


class RedisConfig(BaseSettings):
    host: str
    port: int
    password: Optional[str] = None
    db: int = 0

    @property
    def url(self) -> str:
        url = ConnectionURL(
            "redis",
            host=self.host,
            port=self.port,
            password=self.password,
            path=str(self.db),
        )
        return url.as_string()
