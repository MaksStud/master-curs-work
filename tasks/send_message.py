import asyncio
from typing import Any, List

from core.celery_app.app import celery_app
from services.notifications.registry import NotificationRegistry
from services.notifications.notification_abstract import NotificationAbstract

@celery_app.task
def send_massage(service_name: str, recipients: List[str], content: Any, subject: str | None):
    """
    A Celery task for sending messages.
    
    :service_name: The key to obtaining the notification class.
    :recipients: List of recipients.
    :content: What will be in the message.
    :subject: Subject of the message.
    """
    service: NotificationAbstract = NotificationRegistry.get(service_name)(
        recipients=recipients,
        content=content,
        subject=subject
    )
    asyncio.run(service.send())
