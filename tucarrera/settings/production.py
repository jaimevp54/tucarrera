from __future__ import absolute_import, unicode_literals

from decouple import config
from .base import *

DEBUG = False
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
