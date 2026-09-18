from abc import ABC, abstractmethod
from typing import Any, List


class NotificationAbstract(ABC):
    """An abstract class for sending messages."""
    def __init__(self, recipients: List[str], content: Any, subject: str | None):
        """
        Retrieving data for all classes.
        
        :recipients: List of recipients.
        :content: What will be in the message.
        :subject: Subject of the message.
        """
        self.recipients: List[str] = recipients
        self.content: Any = content
        self.subject: str | None = subject

    @abstractmethod
    def send(self) -> None:
        """A method that must be overridden by every class that inherits from it."""
        raise NotImplementedError("It must be іmplemented in the sub class.")
