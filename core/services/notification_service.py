# File: core/services/notification_service.py
from typing import List, Optional, Any, Dict
from uuid import UUID, uuid4
from datetime import datetime
from core.notification import Notification, NotificationStatus
from core.repositories.notification_repository import NotificationRepository
from core.repositories.channel_repository import ChannelRepository
from core.exceptions import NotificationError, ChannelError


class NotificationService:
    _instance = None

    def __init__(self, notification_repository, channel_repository):
        self.notification_repository = notification_repository
        self.channel_repository = channel_repository

    async def send_notification(self, recipient: str, message: str, channel_type: str) -> Notification:
        try:
            channel = await self.channel_repository.get_by_type(channel_type)
            if not channel:
                raise ChannelError(f"Channel type '{channel_type}' not found.")
            now = datetime.utcnow()
            notification = Notification(
                id=uuid4(),
                recipient=recipient,
                message=message,
                status=NotificationStatus.SENT,
                created_at=now,
                updated_at=now,
            )
            saved = await self.notification_repository.save(notification)
            return saved
        except ChannelError as e:
            raise e
        except Exception as e:
            raise NotificationError(f"Failed to send notification: {e}") from e

    async def get_notification(self, notification_id):
        from core.exceptions import NotificationNotFoundError
        notification = await self.notification_repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError(str(notification_id))
        return notification
