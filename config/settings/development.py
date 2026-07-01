from .base import *  # noqa: F401,F403

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

SECRET_KEY = env(
    'SECRET_KEY',
    default='django-insecure-dev-only-change-in-production',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
