from typing import Literal, Optional

from pydantic import BaseModel, model_validator
from sqlalchemy import URL


class SQLiteSettings(BaseModel):
    path: str

    @property
    def url(self) -> URL:
        return URL.create("sqlite", database=self.path)


class PostgresSettings(BaseModel):
    username: str
    password: str
    db_name: str
    host: str
    port: int
    db_schema: str = "public"  # `schema` is a reserved keyword in SQLAlchemy BaseModel

    @property
    def url(self) -> str:
        url = URL.create(
            "postgresql+asyncpg",
            username=self.username,
            password=self.password,
            host=self.host,
            database=self.db_name,
            port=self.port,
        )
        return url.render_as_string(hide_password=False)


class DBSettings(BaseModel):
    engine: Literal["sqlite", "postgres"]

    # We need a validation to force one of these to be set depending on the engine
    sqlite: Optional[SQLiteSettings] = None
    postgres: Optional[PostgresSettings] = None

    @property
    def url(self) -> str:
        engine_conf = getattr(self, self.engine)
        return engine_conf.url

    @model_validator(mode="after")
    def validate_engine_config(self) -> "DBSettings":
        if getattr(self, self.engine) is None:
            raise ValueError(
                f"Database engine is set to '{self.engine}' but no config provided"
            )
        return self
