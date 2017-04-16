from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': 'autofocus',
            'placeholder': 'Email',
        }),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
        }),
    )

    error_messages = {
        'invalid_login':
            'Please enter a correct email and password. Note that the password '
            'field is case-sensitive.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        email = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
