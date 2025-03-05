from app.adapters.user.microservice_adapter import MicroserviceUserRepository
from app.ports.user_repository import UserRepository


def get_user_repository() -> UserRepository:
    return MicroserviceUserRepository()
