from typing import Any, List

from core.celery import celery_app
from services.notifications.registry import NotificationRegistry


@celery_app.task
def send_massage(service_name: str, recipients: List[str], content: Any, subject: str | None):
    """
    A Celery task for sending messages.
    
    :service_name: The key to obtaining the notification class.
    :recipients: List of recipients.
    :content: What will be in the message.
    :subject: Subject of the message.
    """
    service = NotificationRegistry.get(service_name)(
        recipients=recipients,
        content=content,
        subject=subject
    )
    service.send()

