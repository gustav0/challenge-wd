import logging
from datetime import datetime
from typing import Any, Callable, Optional, override

from fastapi import BackgroundTasks

from app.ports.queue_port import QueuePort

logger = logging.getLogger(__name__)


class FastAPIBackgroundTaskAdapter(QueuePort):
    def __init__(self, background_tasks: BackgroundTasks):
        self.scheduler = background_tasks

    async def schedule_task(
        self,
        task: Callable[..., Any],
        eta: Optional[datetime] = None,
        countdown: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Schedule a task using FastAPI BackgroundTasks.
        """
        logger.info(
            "Attempting to schedule task %s with args %s, kwargs %s, eta %s and countdown %s.",
            task,
            args,
            kwargs,
            eta,
            countdown,
        )
        if eta is not None or countdown is not None:
            logger.warning(
                "eta and countdown are not supported by FastAPIBackgroundTaskAdapter."
                "The tasks will be executed immediately."
            )
        logger.info(
            "Adding background task %s with args %s and kwargs %s",
            task,
            args,
            kwargs,
        )
        if "func" in kwargs:
            task = kwargs.pop("func")

        self.scheduler.add_task(task, *args, **kwargs)
