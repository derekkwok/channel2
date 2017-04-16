from channel2.account.forms import LoginForm
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
