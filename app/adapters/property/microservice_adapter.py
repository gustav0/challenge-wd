from typing import Optional

from app.config import settings
from app.domain.schemas import Property
from app.ports.property_service import PropertyService


class MicroservicePropertyService(PropertyService):
    async def get_property_by_id(self, id: str) -> Optional[Property]:
        """This should be a call to a microservice via httpx request"""
        config = settings.property_service

        # Mock property
        return Property(
            id=id,
            address="123 Main St",
            property_type="House",
            price=100000.0,
        )
