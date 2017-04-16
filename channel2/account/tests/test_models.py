from channel2.account.models import User
from channel2.base.tests import BaseTestCase


class UserManagerTest(BaseTestCase):

    def test_create_superuser(self):
        user = User.objects.create_superuser('newuser@example.com', 'password')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
