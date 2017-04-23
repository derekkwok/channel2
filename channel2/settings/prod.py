from channel2.settings.base import *

ALLOWED_HOSTS = [
    'local.derekkwok.net',
    'channel2.derekkwok.net',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'G:\\channel2.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = 'G:\\media'
