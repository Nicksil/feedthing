"""
users.models
~~~~~~~~~~~~
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models

from core.models import TimeStampedModel


class UserManager(BaseUserManager):
    """
    Manager for User model.
    """
    use_in_migrations = True

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        validate_email(email)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    A model for a single User.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_name = models.CharField(max_length=255, blank=True)

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
        return self.email
