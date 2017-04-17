from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from core.models import TimeStampedModel


class UserManager(BaseUserManager):
    # From: django.db.models.manager.BaseManager [L19:L20]
    #: If set to True the manager will be serialized into migrations and will
    #: thus be available in e.g. RunPython operations
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, TimeStampedModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_name = models.CharField(max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return self.first_name.strip()

    def __repr__(self):
        f_name = '\'{}\''.format(self.first_name) if self.first_name else 'None'
        l_name = '\'{}\''.format(self.last_name) if self.last_name else 'None'

        return '{}(email=\'{}\', password=None, first_name={}, last_name={})'.format(
            self.__class__.__name__,
            self.email,
            f_name,
            l_name,
        )

    def __str__(self):
        return repr(self)
