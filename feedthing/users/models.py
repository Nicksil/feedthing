"""
users.models
~~~~~~~~~~~~
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager
from core.models import TimeStampedModel


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """A model for a single User"""

    # Relationships
    feeds = models.ManyToManyField('feeds.Feed', related_name='users')

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_name = models.CharField(max_length=255, blank=True)

    # Managers
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return self.first_name.strip()

    def __repr__(self):
        return '{}(email=\'{}\', password=None)'.format(
            self.__class__.__name__,
            self.email
        )

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.email)
