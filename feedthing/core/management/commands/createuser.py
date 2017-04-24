"""
core.management.commands.createuser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://github.com/django/django/blob/master/django/contrib/auth/management/commands/createsuperuser.py
"""

import getpass
import sys

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.validators import validate_email
from django.db import DEFAULT_DB_ALIAS


class Command(BaseCommand):
    help = 'Used to create a user.'
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options.get('email', '').strip()
        password = None

        if not email:
            raise CommandError('Must provide email address.')

        try:
            validate_email(email)
        except ValidationError as err:
            self.stderr.write('\n'.join(err.messages))
            sys.exit(1)

        fake_user_data = {'email': email}
        user_data = {}

        try:
            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass('Password (again): ')

                if password != password2:
                    self.stderr.write("Error: Your passwords didn't match.")
                    password = None
                    # Don't validate passwords that don't match.
                    continue

                if password.strip() == '':
                    self.stderr.write('Error: Blank passwords aren\'t allowed.')
                    password = None
                    # Don't validate blank passwords.
                    continue

                try:
                    validate_password(password2, self.UserModel(**fake_user_data))
                except ValidationError as err:
                    self.stderr.write('\n'.join(err.messages))
                    password = None

        except KeyboardInterrupt:
            self.stderr.write('\nOperation cancelled.')
            sys.exit(1)

        user_data['email'] = email
        user_data['password'] = password
        self.UserModel._default_manager.db_manager(DEFAULT_DB_ALIAS).create_user(**user_data)

        self.stdout.write('User created successfully.')
