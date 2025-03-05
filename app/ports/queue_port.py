from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, Optional


class QueuePort(ABC):
    @abstractmethod
    async def schedule_task(
        self,
        task: Callable[..., Any],
        eta: Optional[datetime] = None,
        countdown: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Schedule a task to be executed in the future.
        :param task: The callable task function.
        :param eta: The exact time at which the task should be executed.
        :param countdown: Delay in seconds before executing the task.
        """
        ...
