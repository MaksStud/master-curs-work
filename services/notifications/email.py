from fastapi_mail import MessageSchema

from core.email import mail_app

from services.notifications.notification_abstract import NotificationAbstract
from services.notifications.registry import NotificationRegistry

@NotificationRegistry.register('email')
class EmailNotification(NotificationAbstract):
    """Implements the sending of notifications via email."""
    def __init__(self, recipients, content, subject):
        super().__init__(recipients, content, subject)
        self._mail = mail_app

    async def send(self) -> None:
        """Sends notifications via email."""
        message = MessageSchema(
            subject=self.subject,
            recipients=self.recipients,
            body=self.content,
            subtype="html"
        )

        await self._mail.send_message(message)
