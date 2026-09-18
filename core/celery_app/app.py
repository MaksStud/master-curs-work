from celery import Celery

from core.celery_app.schedule import CELERY_BEAT_SCHEDULE
from core.config import settings


celery_app = Celery(
    main=settings.project_name,
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule=CELERY_BEAT_SCHEDULE
)

