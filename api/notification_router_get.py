# File: api/notification_router_get.py
"""
FastAPI router for retrieving notifications.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Any, Dict

from core.use_cases import GetNotification
from core.exceptions import NotificationNotFoundError
from infrastructure.notification_repository import InMemoryNotificationRepository
from core.use_cases import NotificationRepository

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

def get_notification_repository() -> NotificationRepository:
    """
    Dependency injector for the notification repository.
    """
    return InMemoryNotificationRepository.get_instance()

@router.get(
    "/{notification_id}",
    response_model="NotificationResponse",
    summary="Get Notification by ID",
    description="Retrieves a single notification by its unique identifier."
)
async def get_notification_by_id(
    notification_id: str,
    repo: NotificationRepository = Depends(get_notification_repository)
) -> Dict[str, Any]:
    """
    Endpoint to fetch a notification by its ID.

    It uses the GetNotification use case to retrieve the data and handles
    potential errors, such as the notification not being found.

    Args:
        notification_id: The unique ID of the notification to retrieve.
        repo: The notification repository dependency.

    Returns:
        A dictionary representing the notification.

    Raises:
        HTTPException: 404 if the notification is not found.
        HTTPException: 500 for any other unexpected errors.
    """
    try:
        get_notification_use_case = GetNotification(notification_repository=repo)
        notification = await get_notification_use_case.execute(notification_id=notification_id)
        return notification
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # This is a general catch-all for unexpected errors.
        # In a real application, more specific error handling would be added.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


class NotificationResponse(BaseModel):
    """
    Pydantic model representing the structure of a returned notification.
    """
    id: str
    user_id: str
    message: str
    channel: str
    status: str

python
# File: api/notification_router_get.py
"""
FastAPI router for retrieving notifications.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Any, Dict

from core.use_cases import GetNotification
from core.exceptions import NotificationNotFoundError
from infrastructure.notification_repository import InMemoryNotificationRepository
from core.use_cases import NotificationRepository

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

def get_notification_repository() -> NotificationRepository:
    """
    Dependency injector for the notification repository.
    """
    return InMemoryNotificationRepository.get_instance()

@router.get(
    "/{notification_id}",
    response_model="NotificationResponse",
    summary="Get Notification by ID",
    description="Retrieves a single notification by its unique identifier."
)
async def get_notification_by_id(
    notification_id: str,
    repo: NotificationRepository = Depends(get_notification_repository)
) -> Dict[str, Any]:
    """
    Endpoint to fetch a notification by its ID.

    It uses the GetNotification use case to retrieve the data and handles
    potential errors, such as the notification not being found.

    Args:
        notification_id: The unique ID of the notification to retrieve.
        repo: The notification repository dependency.

    Returns:
        A dictionary representing the notification.

    Raises:
        HTTPException: 404 if the notification is not found.
        HTTPException: 500 for any other unexpected errors.
    """
    try:
        get_notification_use_case = GetNotification(notification_repository=repo)
        notification = await get_notification_use_case.execute(notification_id=notification_id)
        return notification
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # This is a general catch-all for unexpected errors.
        # In a real application, more specific error handling would be added.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


class NotificationResponse(BaseModel):
    """
    Pydantic model representing the structure of a returned notification.
    """
    id: str
    user_id: str
    message: str
    channel: str
    status: str