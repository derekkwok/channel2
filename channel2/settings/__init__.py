# Note: Pylint wildcard-import check is disabled because django relies on settings module
# wildcard-imports.
# pylint: disable=wildcard-import
import os

MODE = os.environ.get('C2_MODE', 'dev')
print('Working in {} mode'.format(MODE))

if MODE == 'dev':
    from .dev import *
elif MODE == 'prod':
    from .prod import *
else:
    raise RuntimeError('Unknown mode: {}'.format(MODE))
