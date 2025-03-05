from app.adapters.property.microservice_adapter import MicroservicePropertyService
from app.ports.property_service import PropertyService


def get_property_service() -> PropertyService:
    return MicroservicePropertyService()
