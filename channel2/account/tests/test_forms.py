from channel2.account.forms import LoginForm, SetPasswordForm
from channel2.account.models import User
from channel2.base.tests import BaseTestCase


class LoginFormTest(BaseTestCase):

    def test_form(self):
        form = LoginForm(data={
            'email': self.user.email,
            'password': self.user.password,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_form_email_case_insensitive(self):
        form = LoginForm(data={
            'email': self.user.email.upper(),
            'password': self.user.password,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_form_fail(self):
        form = LoginForm(data={
            'email': self.user.email,
            'password': 'this-is-a-wrong-password',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'], [LoginForm.error_messages['invalid_login']])

    def test_form_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form = LoginForm(data={
            'email': self.user.email,
            'password': self.user.password,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'], [LoginForm.error_messages['invalid_login']])


class SetPasswordFormTest(BaseTestCase):

    def test_form(self):
        form = SetPasswordForm(user=self.user, data={
            'password1': 'new_password',
            'password2': 'new_password',
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.check_password('new_password'))
        self.assertTrue(user.is_active)
        self.assertEqual(user.token, '')

    def test_password_mismatch(self):
        form = SetPasswordForm(user=self.user, data={
            'password1': '1234',
            'password2': '2345',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password2'],
            [SetPasswordForm.error_messages['password_mismatch']])

    def test_password_empty(self):
        form = SetPasswordForm(user=self.user, data={
            'password1': '',
            'password2': '2345',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password1'],
            ['This field is required.'])
