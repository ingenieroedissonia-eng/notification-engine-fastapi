f = open('infrastructure/repositories/in_memory_channel_repository.py', 'r', encoding='utf-8')
c = f.read()
f.close()

seed = '''
        from core.channel import Channel, ChannelType
        import uuid
        self._channels = {
            'email': Channel(name='Email', type=ChannelType.EMAIL),
            'sms': Channel(name='SMS', type=ChannelType.SMS),
            'push': Channel(name='Push', type=ChannelType.PUSH),
        }
'''

c = c.replace(
    'if InMemoryChannelRepository._instance is not None:\n            raise RuntimeError("Singleton instance already created. Use get_instance().")',
    'if InMemoryChannelRepository._instance is not None:\n            raise RuntimeError("Singleton instance already created. Use get_instance().")' + '\n' + seed
)

f = open('infrastructure/repositories/in_memory_channel_repository.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')