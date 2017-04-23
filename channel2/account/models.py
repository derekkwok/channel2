from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        email = UserManager.normalize_email(email)
        extra_fields.update({
            'is_active': True,
            'is_staff': True,
        })
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
