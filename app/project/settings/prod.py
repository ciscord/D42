"""
website
(c) Device42 <dave.amato@device42.com>

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from project.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
USE_ETAGS = True

ALLOWED_HOSTS = [".device42.com",]

AWS_S3_GZIP_STATIC = True
AWS_S3_SECURE_URLS = False
AWS_IS_GZIPPED = True
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = 'public-read'
AWS_STORAGE_BUCKET_NAME = 'd42cdn'
AWS_SECRET_ACCESS_KEY = 'kOvhzMuq/yuXdxyjhYa7dk6XfXWsI1Q+JaQ0Lkm9'
AWS_ACCESS_KEY_ID = 'AKIAIS2U7NVNTQXL7AMQ'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = 'cdn4.device42.com'
# CLOUDFRONT_URL = 'http://d13skuvfb4lb6j.cloudfront.net/'

STATIC_URL = "http://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
CACHE_MIDDLEWARE_SECONDS = 7200


AWS_HEADERS = {
  'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
  'Cache-Control': 'max-age=94608000',
}

GZIP_CONTENT_TYPES  = (
    'text/css',
    'text/javascript',
    'application/javascript',
    'application/x-javascript',
    'image/svg+xml',
    )
