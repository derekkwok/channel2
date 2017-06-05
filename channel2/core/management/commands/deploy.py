import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

TARGET = 'E:\\channel2'


class Command(BaseCommand):

    def handle(self, *args, **options):
        if os.path.exists(TARGET):
            shutil.rmtree(TARGET)
        ignore = shutil.ignore_patterns('.git', '.idea', '__pycache__')
        shutil.copytree(settings.BASE_DIR, TARGET, ignore=ignore)
        call_command('migrate', interactive=False)
        call_command('collectstatic', interactive=False)
