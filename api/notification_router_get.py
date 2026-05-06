# File: api/notification_router_get.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Any
from core.use_cases import GetNotification
from core.exceptions import NotificationNotFoundError
from infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository
from core.repositories.notification_repository import NotificationRepository


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    message: str
    channel: str
    status: str


router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notification_repository() -> NotificationRepository:
    return InMemoryNotificationRepository.get_instance()


@router.get("/{notification_id}", response_model=NotificationResponse, summary="Get Notification by ID")
async def get_notification_by_id(
    notification_id: str,
    repo: NotificationRepository = Depends(get_notification_repository)
) -> Any:
    try:
        use_case = GetNotification(notification_repository=repo)
        notification = await use_case.execute(notification_id=notification_id)
        return notification
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))