f = open('infrastructure/repositories/in_memory_channel_repository.py', 'r', encoding='utf-8')
c = f.read()
f.close()

nuevo_metodo = '''
    async def get_by_type(self, channel_type: str):
        for channel in self._channels.values():
            if hasattr(channel, 'type') and str(channel.type).upper() == channel_type.upper():
                return channel
        return None
'''

# Insertar antes del ultimo metodo delete
c = c.rstrip()
if 'get_by_type' not in c:
    c = c + '\n' + nuevo_metodo

f = open('infrastructure/repositories/in_memory_channel_repository.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')