import os
from typing import Callable, List, Text

from django.http import request
from django.template import context_processors as django_cp

from channel2.lib import context_processors

BASE_DIR = os.path.abspath(__file__)
for _ in range(3):
    BASE_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = '4y*@!1^$_^$ra*_o*$+@@!bh4dl@fx$n=m0a2qz!x)yc0r6%nh'

DEBUG = False

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channel2.data',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'channel2.urls'

WSGI_APPLICATION = 'channel2.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

TIME_ZONE = 'UTC'
USE_TZ = True

TEST_RUNNER = 'channel2.test.runner.Channel2TestRunner'

JINJA2_DIRS: List[Text] = [
    os.path.join(BASE_DIR, 'templates'),
]
JINJA2_CONTEXT_PROCESSORS: List[Callable[[request.HttpRequest], None]] = [
    django_cp.csrf,
    django_cp.debug,
    django_cp.request,

    context_processors.version,
]
