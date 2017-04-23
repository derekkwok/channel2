import os

mode = os.environ.get('C2_MODE', 'dev')
print('Working in {} mode'.format(mode))

if mode == 'dev':
    from channel2.settings.dev import *
elif mode == 'prod':
    from channel2.settings.prod import *
elif mode == 'test':
    from channel2.settings.test import *
else:
    raise RuntimeError('Unknown mode: {}'.format(mode))
