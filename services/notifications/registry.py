from typing import Dict

from services.notifications.notification_abstract import NotificationAbstract


class NotificationRegistry:
    """Compiles a list of notification services."""
    _registry: Dict[str, type[NotificationAbstract]] = {}

    @classmethod
    def register(cls, name: str):
        """
        A decorator for registering a service in the dictionary.
        
        :name: The key to obtaining the class.
        """
        def wrapper(notification_class):
            cls._registry[name] = notification_class
            return notification_class
        return wrapper

    @classmethod
    def get(cls, name: str) -> type[NotificationAbstract]:
        """
        Returns a class by its key; if the key does not exist, an error is raised.

        :name: The key to obtaining the class.

        :return: class derived from NotificationAbstract.
        """
        if name not in cls._registry:
            raise ValueError(f"Unknown notification type: {name}")
        return cls._registry.get(name)
