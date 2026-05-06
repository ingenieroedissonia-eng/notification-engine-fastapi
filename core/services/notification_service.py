# File: core/services/notification_service.py
"""
This module defines the NotificationService, which orchestrates notification logic.

The service acts as a central point for handling notifications, interacting with
notification and channel repositories to manage the lifecycle of notifications.
"""

from typing import List, Optional, Any, Dict
from uuid import UUID

from core.notification import Notification
from core.channel import Channel
from core.repositories.notification_repository import NotificationRepository
from core.repositories.channel_repository import ChannelRepository
from core.exceptions import NotificationError, ChannelError, InvalidConfigurationError


class NotificationService:
    """
    Service layer for managing notifications.

    This class provides methods to send notifications, retrieve notification history,
    and interact with the underlying data repositories. It follows a singleton
    pattern to ensure a single instance manages the service logic.
    """
    _instance: Optional["NotificationService"] = None

    def __init__(
        self,
        notification_repository: NotificationRepository,
        channel_repository: ChannelRepository
    ) -> None:
        """
        Initializes the NotificationService with necessary repositories.

        Note: This constructor should not be called directly. Use get_instance().

        Args:
            notification_repository: The repository for notification data access.
            channel_repository: The repository for channel data access.
        """
        if self.__class__._instance is not None:
            raise RuntimeError("Use get_instance() to obtain the service instance.")
        self.notification_repository = notification_repository
        self.channel_repository = channel_repository

    @classmethod
    def get_instance(
        cls,
        notification_repository: Optional[NotificationRepository] = None,
        channel_repository: Optional[ChannelRepository] = None
    ) -> "NotificationService":
        """
        Gets the singleton instance of the NotificationService.

        The repositories are required only for the first instantiation.

        Args:
            notification_repository: The repository for notification data access.
            channel_repository: The repository for channel data access.

        Returns:
            The singleton NotificationService instance.

        Raises:
            RuntimeError: If called for the first time without repositories.
        """
        if cls._instance is None:
            if notification_repository is None or channel_repository is None:
                raise RuntimeError(
                    "NotificationRepository and ChannelRepository are required "
                    "for the first instantiation."
                )
            cls._instance = cls(notification_repository, channel_repository)
        return cls._instance

    async def send_notification(
        self,
        recipient: str,
        message: str,
        channel_type: str,
        notification_data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Creates and sends a notification through a specified channel type.

        Args:
            recipient: The recipient of the notification (e.g., email, phone number).
            message: The content of the notification message.
            channel_type: The type of channel to use for sending (e.g., 'EMAIL', 'SMS').
            notification_data: Optional dictionary with additional data for the notification.

        Returns:
            The created Notification object.

        Raises:
            ChannelError: If the specified channel type is not found.
            InvalidConfigurationError: If the channel has no valid configuration.
            NotificationError: For general failures in the notification sending process.
        """
        try:
            # Note: This assumes ChannelRepository has a 'get_by_type' method.
            # This method needs to be added to the repository's interface and implementation.
            channel = await self.channel_repository.get_by_type(channel_type)
            if not channel:
                raise ChannelError(f"Channel type '{channel_type}' not found.")

            if not channel.configuration:
                raise InvalidConfigurationError(f"Channel '{channel_type}' has no configuration.")

            # Note: This assumes the Notification entity constructor accepts these fields.
            # The entity might need to be updated to support 'channel_type' and 'notification_data'.
            notification = Notification(
                recipient=recipient,
                message=message,
                status="PENDING",
                channel_type=channel_type,
                notification_data=notification_data if notification_data else {}
            )
            created_notification = await self.notification_repository.save(notification)
            
            # In a real-world scenario, this is where you would trigger an
            # asynchronous task or event to handle the actual sending via the channel.
            
            return created_notification
        except (ChannelError, InvalidConfigurationError) as e:
            raise e
        except Exception as e:
            raise NotificationError(f"Failed to send notification: {e}") from e

    async def get_notification_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Retrieves a notification by its unique ID.

        Args:
            notification_id: The UUID of the notification to retrieve.

        Returns:
            The Notification object if found, otherwise None.

        Raises:
            NotificationError: If there's an error during retrieval.
        """
        try:
            return await self.notification_repository.get_by_id(notification_id)
        except Exception as e:
            raise NotificationError(f"Failed to retrieve notification {notification_id}: {e}") from e

    async def get_all_notifications(self) -> List[Notification]:
        """
        Retrieves all notifications from the repository.

        Returns:
            A list of all Notification objects.

        Raises:
            NotificationError: If there's an error during retrieval.
        """
        try:
            return await self.notification_repository.get_all()
        except Exception as e:
            raise NotificationError(f"Failed to retrieve all notifications: {e}") from e

# File: core/services/notification_service.py
"""
This module defines the NotificationService, which orchestrates notification logic.

The service acts as a central point for handling notifications, interacting with
notification and channel repositories to manage the lifecycle of notifications.
"""

from typing import List, Optional, Any, Dict
from uuid import UUID

from core.notification import Notification
from core.channel import Channel
from core.repositories.notification_repository import NotificationRepository
from core.repositories.channel_repository import ChannelRepository
from core.exceptions import NotificationError, ChannelError, InvalidConfigurationError


class NotificationService:
    """
    Service layer for managing notifications.

    This class provides methods to send notifications, retrieve notification history,
    and interact with the underlying data repositories. It follows a singleton
    pattern to ensure a single instance manages the service logic.
    """
    _instance: Optional["NotificationService"] = None

    def __init__(
        self,
        notification_repository: NotificationRepository,
        channel_repository: ChannelRepository
    ) -> None:
        """
        Initializes the NotificationService with necessary repositories.

        Note: This constructor should not be called directly. Use get_instance().

        Args:
            notification_repository: The repository for notification data access.
            channel_repository: The repository for channel data access.
        """
        if self.__class__._instance is not None:
            raise RuntimeError("Use get_instance() to obtain the service instance.")
        self.notification_repository = notification_repository
        self.channel_repository = channel_repository

    @classmethod
    def get_instance(
        cls,
        notification_repository: Optional[NotificationRepository] = None,
        channel_repository: Optional[ChannelRepository] = None
    ) -> "NotificationService":
        """
        Gets the singleton instance of the NotificationService.

        The repositories are required only for the first instantiation.

        Args:
            notification_repository: The repository for notification data access.
            channel_repository: The repository for channel data access.

        Returns:
            The singleton NotificationService instance.

        Raises:
            RuntimeError: If called for the first time without repositories.
        """
        if cls._instance is None:
            if notification_repository is None or channel_repository is None:
                raise RuntimeError(
                    "NotificationRepository and ChannelRepository are required "
                    "for the first instantiation."
                )
            cls._instance = cls(notification_repository, channel_repository)
        return cls._instance

    async def send_notification(
        self,
        recipient: str,
        message: str,
        channel_type: str,
        notification_data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Creates and sends a notification through a specified channel type.

        Args:
            recipient: The recipient of the notification (e.g., email, phone number).
            message: The content of the notification message.
            channel_type: The type of channel to use for sending (e.g., 'EMAIL', 'SMS').
            notification_data: Optional dictionary with additional data for the notification.

        Returns:
            The created Notification object.

        Raises:
            ChannelError: If the specified channel type is not found.
            InvalidConfigurationError: If the channel has no valid configuration.
            NotificationError: For general failures in the notification sending process.
        """
        try:
            # Note: This assumes ChannelRepository has a 'get_by_type' method.
            # This method needs to be added to the repository's interface and implementation.
            channel = await self.channel_repository.get_by_type(channel_type)
            if not channel:
                raise ChannelError(f"Channel type '{channel_type}' not found.")

            if not channel.configuration:
                raise InvalidConfigurationError(f"Channel '{channel_type}' has no configuration.")

            # Note: This assumes the Notification entity constructor accepts these fields.
            # The entity might need to be updated to support 'channel_type' and 'notification_data'.
            notification = Notification(
                recipient=recipient,
                message=message,
                status="PENDING",
                channel_type=channel_type,
                notification_data=notification_data if notification_data else {}
            )
            created_notification = await self.notification_repository.save(notification)
            
            # In a real-world scenario, this is where you would trigger an
            # asynchronous task or event to handle the actual sending via the channel.
            
            return created_notification
        except (ChannelError, InvalidConfigurationError) as e:
            raise e
        except Exception as e:
            raise NotificationError(f"Failed to send notification: {e}") from e

    async def get_notification_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Retrieves a notification by its unique ID.

        Args:
            notification_id: The UUID of the notification to retrieve.

        Returns:
            The Notification object if found, otherwise None.

        Raises:
            NotificationError: If there's an error during retrieval.
        """
        try:
            return await self.notification_repository.get_by_id(notification_id)
        except Exception as e:
            raise NotificationError(f"Failed to retrieve notification {notification_id}: {e}") from e

    async def get_all_notifications(self) -> List[Notification]:
        """
        Retrieves all notifications from the repository.

        Returns:
            A list of all Notification objects.

        Raises:
            NotificationError: If there's an error during retrieval.
        """
        try:
            return await self.notification_repository.get_all()
        except Exception as e:
            raise NotificationError(f"Failed to retrieve all notifications: {e}") from e