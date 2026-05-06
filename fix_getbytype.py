f = open('infrastructure/repositories/in_memory_channel_repository.py', 'r', encoding='utf-8')
c = f.read()
f.close()

c = c.replace(
    '''    async def get_by_type(self, channel_type: str):
        for channel in self._channels.values():
            if hasattr(channel, 'type') and str(channel.type).upper() == channel_type.upper():
                return channel
        return None''',
    '''    async def get_by_type(self, channel_type: str):
        search = channel_type.upper()
        for channel in self._channels.values():
            ch_type = str(channel.type.value).upper() if hasattr(channel.type, 'value') else str(channel.type).upper()
            if ch_type == search:
                return channel
        return None'''
)

f = open('infrastructure/repositories/in_memory_channel_repository.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')