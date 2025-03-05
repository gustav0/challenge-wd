import logging

from fastapi import FastAPI

from app.config import settings
from app.entrypoint.rest_api.v1 import notifications, preferences
from app.setup import lifespan

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(
    preferences.router,
    tags=["preferences"],
)
app.include_router(
    notifications.router,
    tags=["notifications"],
)


@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}
