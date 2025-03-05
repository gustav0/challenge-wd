import logging
from typing import Optional

from app.config import settings
from app.domain.schemas import User
from app.ports.user_repository import UserRepository

logger = logging.getLogger(__name__)


class MicroserviceUserRepository(UserRepository):
    async def get_user_by_id(self, id: str) -> Optional[User]:
        """This should be a call to a microservice via httpx request"""
        # This is tighly coupled to the settings.user_repository.
        # We have access to: `config.base_url`, `config.timeout` and `config.api_key`
        config = settings.user_repository
        logger.info(
            f"MicroserviceUserRepository: Fetching user with ID {id} from User MicroService {config=}"
        )

        # Mock some invalid user ids
        try:
            int(id)
        except ValueError:
            return None

        # Mock user
        return User(
            id=id,
            email=f"email.{id}@example.com",
            phone_number="1234567890",
        )
