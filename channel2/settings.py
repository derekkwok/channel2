import os
from typing import Callable, List, Text

from django.http import request
from django.template import context_processors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '4y*@!1^$_^$ra*_o*$+@@!bh4dl@fx$n=m0a2qz!x)yc0r6%nh'

DEBUG = True

ALLOWED_HOSTS: List[Text] = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channel2.apps.web',
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
    }
}

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

TIME_ZONE = 'UTC'
USE_TZ = True

STATIC_URL = '/static/'

TEST_RUNNER = 'channel2.test.runner.Channel2TestRunner'

JINJA2_DIRS: List[Text] = [
    os.path.join(BASE_DIR, 'templates'),
]
JINJA2_CONTEXT_PROCESSORS: List[Callable[[request.HttpRequest], None]] = [
    context_processors.csrf,
    context_processors.debug,
    context_processors.request,
]
