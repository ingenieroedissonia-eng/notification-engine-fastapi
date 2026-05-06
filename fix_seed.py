f = open('infrastructure/repositories/in_memory_channel_repository.py', 'r', encoding='utf-8')
c = f.read()
f.close()

c = c.replace(
    '        self._channels = {}',
    '''        from core.channel import ChannelType
        from uuid import uuid4
        ch_email = Channel(name="Email", type=ChannelType.EMAIL, configuration={})
        ch_sms = Channel(name="SMS", type=ChannelType.SMS, configuration={})
        ch_push = Channel(name="Push", type=ChannelType.PUSH, configuration={})
        self._channels = {
            ch_email.id: ch_email,
            ch_sms.id: ch_sms,
            ch_push.id: ch_push,
        }'''
)

f = open('infrastructure/repositories/in_memory_channel_repository.py', 'w', encoding='utf-8')
f.write(c)
f.close()
print('OK')