import time

import sys

from django.core.management.base import BaseCommand

from channel2.account.models import User


def timed(func):

    def inner(*args, **kwargs):
        start = time.time()
        sys.stdout.write('\t{}'.format(func.__name__))
        sys.stdout.flush()
        result = func(*args, **kwargs)
        duration = int((time.time() - start) * 1000)
        sys.stdout.write(' - {}ms\n'.format(duration))
        return result

    return inner


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('-' * 70)
        print('datacreator.py started')
        start = time.time()

        self.create_users()

        duration = int((time.time() - start) * 1000)
        print('datacreator.py finished in {}ms'.format(duration))
        print('-' * 70)

    @timed
    def create_users(self):
        def create_user_helper(email, **kwargs):
            kwargs['is_active'] = True
            user = User(email=email, **kwargs)
            user.set_password('password')
            user.save()
            return user

        self.user = create_user_helper('testuser@example.com')
        self.staff_user = create_user_helper(
            'staffuser@example.com', is_staff=True)
