from pathlib import Path

import environ
from django.urls import reverse_lazy

from pages.site_content_registry import build_content_sidebar_groups

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-only-change-in-production')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'django_htmx',
    'pages.apps.PagesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pages.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@khodakmetal.com')
QUOTE_NOTIFICATION_EMAIL = env(
    'QUOTE_NOTIFICATION_EMAIL',
    default='khodakmetalsolution@gmail.com',
)

LOGIN_URL = '/admin/login/'

TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'menubar': False,
    'plugins': 'link lists image code',
    'toolbar': 'undo redo | bold italic underline | bullist numlist | link image | code',
    'content_css': False,
    'skin': 'oxide',
}

UNFOLD = {
    'SITE_TITLE': 'KHODAK — Адмінпанель',
    'SITE_HEADER': 'KHODAK Metal Solution',
    'SITE_SUBHEADER': 'Панель керування сайтом зварювальних послуг',
    'SITE_ICON': '/static/images/favicon/favicon.svg',
    'SITE_URL': '/',
    'SHOW_VIEW_ON_SITE': True,
    'COLORS': {
        'primary': {
            '50': 'oklch(97% 0.02 45)',
            '100': 'oklch(94% 0.04 45)',
            '200': 'oklch(88% 0.08 45)',
            '300': 'oklch(78% 0.12 45)',
            '400': 'oklch(68% 0.16 45)',
            '500': 'oklch(59% 0.19 45)',
            '600': 'oklch(52% 0.18 45)',
            '700': 'oklch(45% 0.16 45)',
            '800': 'oklch(38% 0.14 45)',
            '900': 'oklch(32% 0.12 45)',
            '950': 'oklch(24% 0.10 45)',
        },
        'font': {
            'subtle-light': 'var(--color-base-500)',
            'subtle-dark': 'var(--color-base-400)',
            'default-light': 'var(--color-base-600)',
            'default-dark': 'oklch(92% 0.01 250)',
            'important-light': 'var(--color-base-900)',
            'important-dark': 'oklch(98% 0 0)',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'command_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Налаштування',
                'separator': False,
                'items': [
                    {
                        'title': 'Налаштування сайту',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:pages_sitesettings_changelist'),
                    },
                ],
            },
            *[
                {**group, 'separator': idx == 0}
                for idx, group in enumerate(build_content_sidebar_groups())
            ],
            {
                'title': 'Контент',
                'separator': True,
                'items': [
                    {
                        'title': 'Послуги',
                        'icon': 'build',
                        'link': reverse_lazy('admin:pages_service_changelist'),
                    },
                    {
                        'title': 'Портфоліо',
                        'icon': 'photo_library',
                        'link': reverse_lazy('admin:pages_portfolioitem_changelist'),
                    },
                    {
                        'title': 'Блог',
                        'icon': 'article',
                        'link': reverse_lazy('admin:pages_blogpost_changelist'),
                    },
                    {
                        'title': 'FAQ',
                        'icon': 'help',
                        'link': reverse_lazy('admin:pages_faqitem_changelist'),
                    },
                ],
            },
            {
                'title': 'Заявки',
                'separator': True,
                'items': [
                    {
                        'title': 'Заявки',
                        'icon': 'inbox',
                        'link': reverse_lazy('admin:pages_quoterequest_changelist'),
                        'badge': 'pages.admin.new_quote_requests_badge',
                        'badge_variant': 'primary',
                    },
                ],
            },
        ],
    },
}
