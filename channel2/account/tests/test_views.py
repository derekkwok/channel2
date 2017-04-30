from django.urls.base import reverse

from channel2.account.models import User
from channel2.base.tests import BaseTestCase


class LoginViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('account:login')

    def test_get(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_post_invalid(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_post(self):
        self.client.logout()
        response = self.client.post(self.url, {
            'email': self.user.email,
            'password': self.user.password,
        })
        self.assertRedirects(response, reverse('index'))

    def test_post_next(self):
        # TODO implement this test when another view is available.
        pass

    def test_get_authenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))

    def test_post_authenticated(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('index'))


class LogoutViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('account:logout')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('account:login'))

    def test_post_logged_out(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('account:login'))


class ActivateViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user.is_active = False
        self.user.token = 'test-token'
        self.user.save()
        self.url = reverse('account:activate', args=[self.user.token])

    def test_get_active_user(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_get_not_found(self):
        response = self.client.get(reverse('account:activate', args=['bad']))
        self.assertEqual(response.status_code, 404)
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/activate.html')

    def test_post_active_user(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_post_not_found(self):
        response = self.client.post(reverse('account:activate', args=['bad']))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post(self.url, {
            'password1': 'new_password',
            'password2': 'new_password',
        })
        self.assertRedirects(response, reverse('index'))
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('new_password'))
