from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u6)oy68q12u8o907d173oo9jnap3=dmkdktsqjufoode(_7vg='


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
