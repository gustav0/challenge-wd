import logging
from datetime import datetime
from typing import Any, Callable, Optional

from app.adapters.queue.celery_adapter.tasks import dispatch_notification_task
from app.ports.queue_port import QueuePort

logger = logging.getLogger(__name__)


# This Adapter is not functional, as the project doesn't support Celery yet.
class CeleryAdapter(QueuePort):
    async def schedule_task(
        self,
        task: Callable[..., Any],
        eta: Optional[datetime] = None,
        countdown: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        logger.info(
            "Celery Adapter: attempting to schedule \ntask %s \neta %s \ncountdown %s \nwith \nargs %s \nkwargs %s",
            task.__name__,
            eta,
            countdown,
            args,
            kwargs,
        )

        task_map = {
            "dispatch_notification": dispatch_notification_task,
        }

        func: Callable[..., Any] = task_map[task.__name__]
        func.s(*args, **kwargs).apply_async(  # type: ignore[attr-defined]
            eta=eta,
        )
