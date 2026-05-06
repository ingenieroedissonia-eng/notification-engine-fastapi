from typing import Dict, List, Optional
from uuid import UUID
from core.notification import Notification
from core.repositories.notification_repository import NotificationRepository
from core.exceptions import NotificationNotFoundError


class InMemoryNotificationRepository(NotificationRepository):
    _instance = None

    def __init__(self):
        if InMemoryNotificationRepository._instance is not None:
            raise RuntimeError("Use get_instance()")
        from uuid import UUID
        from datetime import datetime
        from core.notification import NotificationStatus
        seed_id = UUID("00000000-0000-0000-0000-000000000001")
        seed = Notification(
            id=seed_id,
            recipient="demo@maiie-systems.com",
            message="Notificacion de demo generada por M.A.I.I.E. Systems",
            status=NotificationStatus.SENT,
            created_at=datetime(2026, 1, 1, 0, 0, 0),
            updated_at=datetime(2026, 1, 1, 0, 0, 0),
        )
        self._notifications: Dict[UUID, Notification] = {seed_id: seed}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def save(self, notification: Notification) -> Notification:
        self._notifications[notification.id] = notification
        return notification

    async def get_by_id(self, notification_id) -> Optional[Notification]:
        return self._notifications.get(notification_id)

    async def get_all(self) -> List[Notification]:
        return list(self._notifications.values())

    async def update(self, notification: Notification) -> None:
        self._notifications[notification.id] = notification

    async def delete(self, notification_id) -> None:
        if notification_id in self._notifications:
            del self._notifications[notification_id]
        else:
            raise NotificationNotFoundError(str(notification_id))