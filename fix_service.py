f = open('core/use_cases/create_notification.py', 'r', encoding='utf-8')
c = f.read()
f.close()

# Deduplicar archivo
if c.count('class CreateNotification:') > 1:
    idx = c.index('class CreateNotification:')
    idx2 = c.index('class CreateNotification:', idx + 1)
    c = c[:idx2].strip() + '\n'

# Cambiar channel_id por channel_type en execute y en llamada al service
c = c.replace(
    'async def execute(self, recipient: str, message: str, channel_id: UUID) -> Notification:',
    'async def execute(self, recipient: str, message: str, channel_id: str) -> Notification:'
)
c = c.replace(
    'channel_id=channel_id',
    'channel_type=channel_id'
)

f = open('core/use_cases/create_notification.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK: create_notification.py corregido')