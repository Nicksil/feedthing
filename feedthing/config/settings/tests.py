from .common import *

DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ('rest_framework.authentication.SessionAuthentication',)
TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['debug'] = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    }
}

# Note: Be sure `TEMPLATES[0]['APP_DIRS'] = False` is set.
TEMPLATES[0]['OPTIONS']['loaders'] = [(
    'django.template.loaders.cached.Loader',
    [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ],
)]
