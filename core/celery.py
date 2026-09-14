from celery import Celery
from core.config import settings

celery_app = Celery(
    main=settings.project_name,
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["task"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)

