f = open('api/notification_router.py', 'r', encoding='utf-8')
c = f.read()
f.close()

c = c.replace(
    'notification_repo = InMemoryNotificationRepository()',
    'notification_repo = InMemoryNotificationRepository.get_instance()'
)
c = c.replace(
    'return CreateNotification(repository=notification_repo)',
    'from core.services.notification_service import NotificationService\n    svc = NotificationService(notification_repo)\n    return CreateNotification(notification_service=svc)'
)
c = c.replace(
    'return GetNotification(repository=notification_repo)',
    'return GetNotification(notification_repository=notification_repo)'
)

f = open('api/notification_router.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')