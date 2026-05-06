from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
# File: api/notification_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from core.notification import Notification
from core.use_cases.create_notification import CreateNotification
from core.use_cases.get_notification import GetNotification
from core.exceptions import NotificationError, NotificationNotFoundError
from infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository
from infrastructure.repositories.in_memory_channel_repository import InMemoryChannelRepository
from core.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])
limiter = Limiter(key_func=get_remote_address)

notification_repo = InMemoryNotificationRepository.get_instance()
channel_repo = InMemoryChannelRepository.get_instance()

def get_create_notification_use_case() -> CreateNotification:
    svc = NotificationService(notification_repository=notification_repo, channel_repository=channel_repo)
    return CreateNotification(notification_service=svc)

def get_get_notification_use_case() -> GetNotification:
    return GetNotification(notification_repository=notification_repo)

class CreateNotificationRequest(BaseModel):
    recipient: str = Field(..., example="user@example.com")
    message: str = Field(..., example="Your order has been shipped.")
    channel: str = Field(default="email", example="email")

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
@limiter.limit("2/day")
async def create_notification(request: Request,
    request: CreateNotificationRequest,
    use_case: CreateNotification = Depends(get_create_notification_use_case),
):
    try:
        notification = await use_case.execute(
            recipient=request.recipient,
            message=request.message,
            channel_id=request.channel
        )
        return notification
    except NotificationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{notification_id}", response_model=Notification)
async def get_notification_by_id(
    notification_id: str,
    use_case: GetNotification = Depends(get_get_notification_use_case),
):
    try:
        notification = await use_case.execute(notification_id=notification_id)
        return notification
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
