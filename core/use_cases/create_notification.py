# File: core/use_cases/create_notification.py
"""
Use Case for creating and sending a notification.
"""

from uuid import UUID
from core.notification import Notification
from core.services.notification_service import NotificationService


class CreateNotification:
    """
    This use case handles the creation and sending of a notification.
    It orchestrates the process by using the NotificationService.
    """

    def __init__(self, notification_service: NotificationService):
        """
        Initializes the CreateNotification use case.

        Args:
            notification_service: An instance of NotificationService to handle
                                  the business logic of notifications.
        """
        self.notification_service = notification_service

    async def execute(self, recipient: str, message: str, channel_id: str) -> Notification:
        """
        Executes the use case to create and send a notification.

        Args:
            recipient: The recipient of the notification (e.g., email address, phone number).
            message: The content of the notification message.
            channel_id: The ID of the channel through which to send the notification.

        Returns:
            The created Notification entity.
            
        Raises:
            ChannelError: If the specified channel does not exist.
            NotificationError: For general notification-related errors during creation or sending.
        """
        notification = await self.notification_service.send_notification(
            recipient=recipient,
            message=message,
            channel_type=channel_id
        )
        return notification

# File: core/use_cases/create_notification.py
"""
Use Case for creating and sending a notification.
"""

from uuid import UUID
from core.notification import Notification
from core.services.notification_service import NotificationService
