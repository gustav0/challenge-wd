import logging
from typing import Optional

from fastapi import BackgroundTasks

from app.adapters.queue.celery_adapter import CeleryAdapter
from app.adapters.queue.fastapi_background_task_adapter import (
    FastAPIBackgroundTaskAdapter,
)
from app.config import settings
from app.ports.queue_port import QueuePort

logger = logging.getLogger(__name__)
config = settings.queue

logger.info("Startup: Using queue adapter %s", config.service)


def get_queue_adapter(
    background_tasks: Optional[BackgroundTasks] = None,
) -> QueuePort:
    if config.service == "celery":

        return CeleryAdapter()
    elif config.service == "fastapi":
        if not isinstance(background_tasks, BackgroundTasks):
            raise ValueError(
                "You must provide a BackgroundTasks instance to use FastAPI queue"
            )
        return FastAPIBackgroundTaskAdapter(background_tasks=background_tasks)

    raise ValueError(f"Invalid queue service type: {config.service}")
