from .base import *


DEBUG = True



ALLOWED_HOSTS = ['*']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')