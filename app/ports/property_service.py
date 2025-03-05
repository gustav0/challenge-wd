from abc import ABC, abstractmethod
from typing import Optional

from app.domain.schemas import Property


class PropertyService(ABC):

    @abstractmethod
    async def get_property_by_id(
        self,
        id: str,
    ) -> Optional[Property]:  # pragma: no cover
        """Fetch a property from the PropertyService (different microservice)"""
        ...
