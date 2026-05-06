# File: api/notification_router.py
"""
API Router for handling notification-related operations.

This module defines the endpoints for creating and retrieving notifications.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from core.notification import Notification
from core.use_cases.create_notification import CreateNotification
from core.use_cases.get_notification import GetNotification
from core.exceptions import NotificationError, NotificationNotFoundError
from infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

# A single in-memory repository instance is used to maintain state across API calls.
# In a real application, this would be managed by a more sophisticated dependency
# injection container and connected to a persistent database.
notification_repo = InMemoryNotificationRepository.get_instance()

# --- Dependency Injection Providers ---

def get_create_notification_use_case() -> CreateNotification:
    """
    Dependency provider for the CreateNotification use case.
    """
    from core.services.notification_service import NotificationService
    svc = NotificationService(notification_repo)
    return CreateNotification(notification_service=svc)

def get_get_notification_use_case() -> GetNotification:
    """
    Dependency provider for the GetNotification use case.
    """
    return GetNotification(notification_repository=notification_repo)

# --- Data Transfer Objects (DTOs) ---

class CreateNotificationRequest(BaseModel):
    """
    Request model for creating a new notification.
    """
    recipient: str = Field(
        ...,
        description="The recipient of the notification (e.g., email address, phone number).",
        example="user@example.com"
    )
    message: str = Field(
        ...,
        description="The content of the notification message.",
        example="Your order has been shipped."
    )

# --- API Endpoints ---

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(
    request: CreateNotificationRequest,
    use_case: CreateNotification = Depends(get_create_notification_use_case),
):
    """
    Creates a new notification.

    - **recipient**: The target identifier for the notification (e.g., email).
    - **message**: The content of the message to be sent.
    """
    try:
        notification = use_case.execute(
            recipient=request.recipient,
            message=request.message
        )
        return notification
    except NotificationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/{notification_id}", response_model=Notification)
async def get_notification_by_id(
    notification_id: str,
    use_case: GetNotification = Depends(get_get_notification_use_case),
):
    """
    Retrieves a single notification by its unique ID.
    """
    try:
        notification = use_case.execute(notification_id=notification_id)
        return notification
    except NotificationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )