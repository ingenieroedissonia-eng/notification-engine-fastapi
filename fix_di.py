f = open('api/notification_router.py', 'r', encoding='utf-8')
c = f.read()
f.close()

# Agregar import channel repository
if 'InMemoryChannelRepository' not in c:
    c = c.replace(
        'from infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository',
        'from infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository\nfrom infrastructure.repositories.in_memory_channel_repository import InMemoryChannelRepository'
    )

# Corregir instancia singleton
c = c.replace(
    'notification_repo = InMemoryNotificationRepository.get_instance()',
    'notification_repo = InMemoryNotificationRepository.get_instance()\nchannel_repo = InMemoryChannelRepository.get_instance()'
)

# Corregir service con dos repositorios
c = c.replace(
    'svc = NotificationService(notification_repo)',
    'svc = NotificationService(notification_repository=notification_repo, channel_repository=channel_repo)'
)

f = open('api/notification_router.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')