"""
website
(c) Device42 <dave.amato@device42.com>

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _
#from django.conf import global_settings

#DEBUG = True
ADMINS = (
  ('Raj','raj@rajlog.com'),
  ('Dave','dave.amato@device42.com'),
)
# Directory of the current base directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Secret key. Must be kept secret.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# URL config file.
ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

# Installed apps.
INSTALLED_APPS = (
  # 'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  #'collectfast',
  'django.contrib.staticfiles',
  'storages',
  'project.apps.device42',
  # 'project.apps.device42_abtests',
)


MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'default': None,
    'sessions': None,
    'core': None,
    'profiles': None,
    'snippets': None,
    'scaffold_templates': None,
}

# Middleware classes.
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
if 'prod' in os.environ['DJANGO_SETTINGS_MODULE']:
  MIDDLEWARE_CLASSES += ('django.middleware.cache.UpdateCacheMiddleware',)
MIDDLEWARE_CLASSES += (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.environ['DJANGO_DB_NAME'],
    'USER': os.environ['DJANGO_DB_USER'],
    'PASSWORD': os.environ['DJANGO_DB_PASS'],
    'HOST': os.environ['DJANGO_DB_HOST'],
    'PORT': os.environ['DJANGO_DB_PORT'],
  }
}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# The file storage engine to use when collecting static files with the collectstatic management command.
# https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-STATICFILES_STORAGE
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': (os.path.join(BASE_DIR, 'templates'),),
    'APP_DIRS': False,
  	'OPTIONS': {
  	    'context_processors': [
          # 'django.contrib.auth.context_processors.auth',
          'django.template.context_processors.debug',
          'django.template.context_processors.i18n',
          'django.template.context_processors.request',
          # 'django.template.context_processors.media',
          # 'django.template.context_processors.static',
          'django.template.context_processors.tz',
          'django.contrib.messages.context_processors.messages',
          "project.apps.device42.template_processor_i18n.check_translated",
          "project.apps.device42.template_processor_i18n.set_d42_language",
          "project.apps.device42.template_processor_i18n.set_d42_locale_url",
          "project.apps.device42.template_processor_i18n.site_url",
  	    ],
  	},
  },
]

TEMPLATE_CONTENT_URLS = os.path.join(BASE_DIR, 'templates')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
      'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse'
      }
    },
    'handlers': {
        'mail_admins': {
          'level': 'ERROR',
          #'filters': ['require_debug_false'],
          'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
SERVER_EMAIL = 'website-errors@device42.com'

# POSTMARK
EMAIL_HOST = 'smtp.postmarkapp.com'
EMAIL_HOST_USER = '982fce19-1f7d-4668-9bfe-aa39ae429825'
EMAIL_HOST_PASSWORD = '982fce19-1f7d-4668-9bfe-aa39ae429825'
POSTMARK_API_KEY = '982fce19-1f7d-4668-9bfe-aa39ae429825'
POSTMARK_SENDER = 'support@device42.com'
POSTMARK_TEST_MODE = False

# TWITTER
TWITTER_OAUTH_TOKEN = '286430864-4wXBTPGaeaItJqWYzA6ZHqZO5QhAnXh3I3yRwWuC'
TWITTER_OAUTH_SECRET = '35qG8xW7fhzv11RaSnR1FJ0WiLjWQvE7ZxYi1btY'
TWITTER_CONSUMER_KEY = 'Zui7lWzRUK6cUek58OUvhg'
TWITTER_CONSUMER_SECRET = 'dP8Lu3ZAO9GdlbLUV49x9Ztp5p7sUoaK5DUcNG3MbCA'

# reCAPTCHA
GOOGLE_RECAPTCHA_SITE_KEY = '6Lfs5SMTAAAAAG5H_Gkz48BR4G-iQQBSs5QZdwZH'
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lfs5SMTAAAAAPLPbonH1sm4NpO4XSoNIVMh8OCT'
GOOGLE_RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

INTERNAL_IPS = [
  '0.0.0.0',
  '127.0.0.1',
]

STATIC_DOMAIN = ''

D42_REQUEST_QUOTE_100 = 'https://registration.device42.com/order/D42100/'
D42_REQUEST_QUOTE_500 = 'https://registration.device42.com/order/D42500/'
D42_REQUEST_QUOTE_1000 = 'https://registration.device42.com/order/D421000/'
D42_REQUEST_QUOTE_2500 = 'https://registration.device42.com/order/D422500/'
D42_DOCS_SITE = 'http://docs.device42.com/'
D42_BLOG_SITE = 'http://www.device42.com/blog/'
D42_APIDOCS_SITE = 'http://api.device42.com'


LANGUAGES = (
  ('en', _('English')),
)
AWS_PRELOAD_METADATA = True
