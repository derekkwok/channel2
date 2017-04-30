from channel2.settings.base import *

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = 'E:\\media'
