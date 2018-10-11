from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

ALLOWED_HOSTS = [
    'channel2.derekkwok.net',
]

DATABASES['default']['NAME'] = '/var/www/channel2/db/db.sqlite3'

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/channel2/static'
STATICFILES_DIRS: List[Text] = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media'
MEDIA_ROOT = '/var/www/channel2/media'
