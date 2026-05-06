# Reescribir notification_router.py limpio con rate limiting correcto
router_content = '''from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import APIRouter, Depends, HTTPException, status, Request
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

def get_svc():
    return NotificationService(notification_repository=notification_repo, channel_repository=channel_repo)

def get_create_use_case() -> CreateNotification:
    return CreateNotification(notification_service=get_svc())

def get_get_use_case() -> GetNotification:
    return GetNotification(notification_service=get_svc())

class CreateNotificationRequest(BaseModel):
    recipient: str = Field(..., example="user@example.com")
    message: str = Field(..., example="Your order has been shipped.")
    channel: str = Field(default="email", example="email")

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
@limiter.limit("2/day")
async def create_notification(
    request: Request,
    body: CreateNotificationRequest,
    use_case: CreateNotification = Depends(get_create_use_case),
):
    try:
        notification = await use_case.execute(
            recipient=body.recipient,
            message=body.message,
            channel_id=body.channel
        )
        return notification
    except NotificationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{notification_id}", response_model=Notification)
async def get_notification_by_id(
    notification_id: str,
    use_case: GetNotification = Depends(get_get_use_case),
):
    try:
        from uuid import UUID
        notification = await use_case.execute(notification_id=UUID(notification_id))
        return notification
    except NotificationError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
'''
open('api/notification_router.py', 'w', encoding='utf-8').write(router_content)
print('OK: notification_router.py reescrito')

# Agregar get_notification al service
f = open('core/services/notification_service.py', 'r', encoding='utf-8')
c = f.read()
f.close()

if 'get_notification' not in c:
    nuevo = '''
    async def get_notification(self, notification_id):
        from core.exceptions import NotificationNotFoundError
        notification = await self.notification_repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError(str(notification_id))
        return notification
'''
    c = c.rstrip() + '\n' + nuevo
    open('core/services/notification_service.py', 'w', encoding='utf-8').write(c)
    print('OK: get_notification agregado al service')

print('Todo listo.')