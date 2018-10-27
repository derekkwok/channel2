from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS: List[Text] = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
