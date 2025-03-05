from celery import Celery  # type: ignore

from app.config import settings

config = settings.queue.celery

if config is None:
    raise ValueError("Celery configuration is missing")

celery_app = Celery(
    __name__,
    broker=config.broker_url,
    backend=config.result_backend,
)

celery_app.conf.update(
    task_serializer=config.task_serializer,
    accept_content=config.accept_content,
    timezone=config.timezone,
)

celery_app.autodiscover_tasks(
    packages=["app.adapters.queue.celery_adapter.tasks"],
)
