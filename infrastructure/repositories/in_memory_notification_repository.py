# File: infrastructure/repositories/in_memory_notification_repository.py
"""
In-memory implementation of the NotificationRepository.
"""
from typing import Dict, List, Optional
from uuid import UUID

from core.exceptions import NotificationError
from core.notification import Notification
from core.repositories.notification_repository import NotificationRepository


class InMemoryNotificationRepository(NotificationRepository):
    """
    Implements the NotificationRepository interface using an in-memory dictionary.

    This class uses a singleton pattern to ensure that a single instance
    of the repository is used throughout the application's lifecycle.
    """
    _instance: Optional["InMemoryNotificationRepository"] = None
    _notifications: Dict[UUID, Notification]

    def __init__(self):
        """
        Initializes the repository.

        Raises:
            RuntimeError: If an instance already exists, to enforce the singleton pattern.
        """
        if InMemoryNotificationRepository._instance is not None:
            raise RuntimeError("Use get_instance() to get the singleton instance.")
        self._notifications = {}

    @classmethod
    def get_instance(cls) -> "InMemoryNotificationRepository":
        """
        Returns the singleton instance of the repository.

        If an instance does not exist, it creates one.

        Returns:
            The singleton InMemoryNotificationRepository instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def save(self, notification: Notification) -> None:
        """
        Saves a notification to the in-memory store.

        Args:
            notification: The Notification object to save.

        Raises:
            NotificationError: If the notification ID is not a valid UUID.
        """
        if not isinstance(notification.id, UUID):
            raise NotificationError("Notification ID must be a UUID.")
        self._notifications[notification.id] = notification

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Retrieves a notification by its unique identifier.

        Args:
            notification_id: The UUID of the notification to retrieve.

        Returns:
            The Notification object if found, otherwise None.
        """
        return self._notifications.get(notification_id)

    async def get_all(self) -> List[Notification]:
        """
        Retrieves all notifications from the store.

        Returns:
            A list of all stored Notification objects.
        """
        return list(self._notifications.values())

    async def delete(self, notification_id: UUID) -> None:
        """
        Deletes a notification by its unique identifier.

        If the notification ID does not exist, this method does nothing.

        Args:
            notification_id: The UUID of the notification to delete.
        """
        if notification_id in self._notifications:
            del self._notifications[notification_id]

python
# File: infrastructure/repositories/in_memory_notification_repository.py
"""
In-memory implementation of the NotificationRepository.
"""
from typing import Dict, List, Optional
from uuid import UUID

from core.exceptions import NotificationError
from core.notification import Notification
from core.repositories.notification_repository import NotificationRepository


class InMemoryNotificationRepository(NotificationRepository):
    """
    Implements the NotificationRepository interface using an in-memory dictionary.

    This class uses a singleton pattern to ensure that a single instance
    of the repository is used throughout the application's lifecycle.
    """
    _instance: Optional["InMemoryNotificationRepository"] = None
    _notifications: Dict[UUID, Notification]

    def __init__(self):
        """
        Initializes the repository.

        Raises:
            RuntimeError: If an instance already exists, to enforce the singleton pattern.
        """
        if InMemoryNotificationRepository._instance is not None:
            raise RuntimeError("Use get_instance() to get the singleton instance.")
        self._notifications = {}

    @classmethod
    def get_instance(cls) -> "InMemoryNotificationRepository":
        """
        Returns the singleton instance of the repository.

        If an instance does not exist, it creates one.

        Returns:
            The singleton InMemoryNotificationRepository instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def save(self, notification: Notification) -> None:
        """
        Saves a notification to the in-memory store.

        Args:
            notification: The Notification object to save.

        Raises:
            NotificationError: If the notification ID is not a valid UUID.
        """
        if not isinstance(notification.id, UUID):
            raise NotificationError("Notification ID must be a UUID.")
        self._notifications[notification.id] = notification

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Retrieves a notification by its unique identifier.

        Args:
            notification_id: The UUID of the notification to retrieve.

        Returns:
            The Notification object if found, otherwise None.
        """
        return self._notifications.get(notification_id)

    async def get_all(self) -> List[Notification]:
        """
        Retrieves all notifications from the store.

        Returns:
            A list of all stored Notification objects.
        """
        return list(self._notifications.values())

    async def delete(self, notification_id: UUID) -> None:
        """
        Deletes a notification by its unique identifier.

        If the notification ID does not exist, this method does nothing.

        Args:
            notification_id: The UUID of the notification to delete.
        """
        if notification_id in self._notifications:
            del self._notifications[notification_id]