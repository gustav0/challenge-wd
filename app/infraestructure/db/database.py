from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


class PostgresDBEngineCreator:
    @classmethod
    def create_db_connection_url(cls) -> str:
        return settings.database.postgres.url  # type: ignore[union-attr]

    @classmethod
    def create_db_engine(cls) -> AsyncEngine:
        url = cls.create_db_connection_url()
        return create_async_engine(url)


class SQLiteDBEngineCreator:
    @classmethod
    def create_db_engine(cls) -> AsyncEngine:
        return create_async_engine(settings.database.sqlite.path)  # type: ignore[union-attr]


def get_db_engine() -> AsyncEngine:
    # Supporting multiple DB engines should be done here
    if settings.database.engine == "sqlite":
        return SQLiteDBEngineCreator().create_db_engine()
    elif settings.database.engine == "postgres":
        return PostgresDBEngineCreator().create_db_engine()
    else:
        raise ValueError(f"Unknown database engine: {settings.database.engine}")


def create_session_class() -> async_sessionmaker[AsyncSession]:
    engine = get_db_engine()
    return async_sessionmaker(bind=engine, expire_on_commit=False)


# This is not the session class itself, but a session factory.
Session = create_session_class()
