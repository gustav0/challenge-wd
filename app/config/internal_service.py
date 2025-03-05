from pydantic_settings import BaseSettings


class UserRepositoryConfig(BaseSettings):
    base_url: str
    timeout: int
    api_key: str  # I am just assuming we need some sort of authentication


class PropertiesServiceConfig(BaseSettings):
    base_url: str
    timeout: int
    api_key: str
