# File: core/use_cases/get_notification.py
"""
This module contains the use case for retrieving a specific notification.
"""

from uuid import UUID
from core.notification import Notification
from core.services.notification_service import NotificationService
from core.exceptions import NotificationError

class GetNotification:
    """
    Use case to retrieve a specific notification by its ID.
    """

    def __init__(self, notification_service: NotificationService):
        """
        Initializes the GetNotification use case.

        Args:
            notification_service: The service responsible for handling notification logic.
        """
        self.notification_service = notification_service

    async def execute(self, notification_id: UUID) -> Notification:
        """
        Executes the use case to fetch a notification.

        Args:
            notification_id: The unique identifier of the notification to retrieve.

        Returns:
            The requested Notification entity.

        Raises:
            NotificationError: If the notification is not found or if any other
                               domain-specific error occurs during retrieval.
        """
        try:
            notification = await self.notification_service.get_notification(notification_id)
            if notification is None:
                raise NotificationError(f"Notification with ID {notification_id} not found.")
            return notification
        except NotificationError as e:
            # Propagate domain-specific exceptions from the service layer.
            raise e
        except Exception as e:
            # Wrap unexpected exceptions into a domain-specific error to avoid
            # leaking implementation details.
            raise NotificationError(
                f"An unexpected error occurred while retrieving notification {notification_id}: {e}"
            ) from e

# File: core/use_cases/get_notification.py
"""
This module contains the use case for retrieving a specific notification.
"""

from uuid import UUID
from core.notification import Notification
from core.services.notification_service import NotificationService
from core.exceptions import NotificationError

class GetNotification:
    """
    Use case to retrieve a specific notification by its ID.
    """

    def __init__(self, notification_service: NotificationService):
        """
        Initializes the GetNotification use case.

        Args:
            notification_service: The service responsible for handling notification logic.
        """
        self.notification_service = notification_service

    async def execute(self, notification_id: UUID) -> Notification:
        """
        Executes the use case to fetch a notification.

        Args:
            notification_id: The unique identifier of the notification to retrieve.

        Returns:
            The requested Notification entity.

        Raises:
            NotificationError: If the notification is not found or if any other
                               domain-specific error occurs during retrieval.
        """
        try:
            notification = await self.notification_service.get_notification(notification_id)
            if notification is None:
                raise NotificationError(f"Notification with ID {notification_id} not found.")
            return notification
        except NotificationError as e:
            # Propagate domain-specific exceptions from the service layer.
            raise e
        except Exception as e:
            # Wrap unexpected exceptions into a domain-specific error to avoid
            # leaking implementation details.
            raise NotificationError(
                f"An unexpected error occurred while retrieving notification {notification_id}: {e}"
            ) from e