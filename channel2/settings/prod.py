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

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/channel2/media'

VERSION = open('/var/www/channel2/version.txt').read().strip()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}][{asctime}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/www/channel2/logs/info.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
