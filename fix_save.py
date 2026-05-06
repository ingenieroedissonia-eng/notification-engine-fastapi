f = open('infrastructure/repositories/in_memory_notification_repository.py', 'r', encoding='utf-8')
c = f.read()
f.close()

# Deduplicar
if c.count('class InMemoryNotificationRepository') > 1:
    idx = c.index('class InMemoryNotificationRepository')
    idx2 = c.index('class InMemoryNotificationRepository', idx + 1)
    c = c[:idx2].strip() + '\n'

# Corregir save para que retorne la notificacion
c = c.replace(
    'async def save(self, notification: Notification) -> None:',
    'async def save(self, notification: Notification) -> Notification:'
)

# Asegurar que el save almacena y retorna
import re
def fix_save_body(m):
    return m.group(0)

# Buscar el cuerpo del save y agregar return
lines = c.split('\n')
new_lines = []
in_save = False
save_indent = ''
for i, line in enumerate(lines):
    if 'async def save(self, notification: Notification) -> Notification:' in line:
        in_save = True
        save_indent = '        '
        new_lines.append(line)
        continue
    if in_save:
        if line.strip() == '' and i + 1 < len(lines) and lines[i+1].strip().startswith('async def'):
            new_lines.append(f'{save_indent}    self._notifications[notification.id] = notification')
            new_lines.append(f'{save_indent}    return notification')
            new_lines.append(line)
            in_save = False
            continue
        if line.strip().startswith('async def') or line.strip().startswith('@'):
            new_lines.append(f'{save_indent}    self._notifications[notification.id] = notification')
            new_lines.append(f'{save_indent}    return notification')
            in_save = False
        new_lines.append(line)
    else:
        new_lines.append(line)

c = '\n'.join(new_lines)

f = open('infrastructure/repositories/in_memory_notification_repository.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')