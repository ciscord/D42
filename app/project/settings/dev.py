"""
website
(c) Device42 <dave.amato@device42.com>

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from project.settings.base import *

# Root directory of the entire project.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Directory of the app directory.
APP_DIR = os.path.join(PROJECT_DIR, 'app')

# Directory of the build directory.
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')

# Directory of the temporary directory.
TMP_DIR = os.path.join(PROJECT_DIR, '.tmp')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: change this to more specific hosts in production!
ALLOWED_HOSTS = ['*']

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BUILD_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(TMP_DIR, 'static'),)
