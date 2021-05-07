from homie.settings.local import *
from portfolio import secret_util

"""
These settings is used by App Engine Live. 
"""

MODE = Mode.LIVE
DEBUG = False

print(f"base dir: {BASE_DIR}")

SECRET_KEY = secret_util.get_latest('LIVE_DJANGO_SECRET')

ALLOWED_HOSTS = [
    "127.0.0.1",
    "homie-mt-2021-live.et.r.appspot.com",
    "homie-mt-2021-live.appspot.com",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': secret_util.get_latest('LIVE_DB_HOST'),
        'USER': secret_util.get_latest('LIVE_DB_USER'),
        'PASSWORD': secret_util.get_latest('LIVE_DB_PASSWORD'),
        'NAME': secret_util.get_latest('LIVE_DB_NAME')
    }
}

DEFAULT_ADMIN_USERNAME = secret_util.get_latest('LIVE_DEFAULT_ADMIN_USERNAME')
DEFAULT_ADMIN_PASSWORD = secret_util.get_latest('LIVE_DEFAULT_ADMIN_PASSWORD')

DEBUG_PROPAGATE_EXCEPTIONS = True # todo: testing only, remove this later