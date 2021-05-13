from homie.settings.local import *
from portfolio import secret_util

"""
These settings is used by CI and App Engine Test. 
"""

MODE = Mode.TEST

print(f"base dir: {BASE_DIR}")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "homie-mt-2021.et.r.appspot.com",
    "homie-mt-2021.appspot.com",
    "homie-test.minhthai.me",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': secret_util.get_latest('TEST_DB_HOST'),
        'USER': secret_util.get_latest('TEST_DB_USER'),
        'PASSWORD': secret_util.get_latest('TEST_DB_PASSWORD'),
        'NAME': secret_util.get_latest('TEST_DB_NAME')
    }
}

DEFAULT_ADMIN_USERNAME = secret_util.get_latest('TEST_DEFAULT_ADMIN_USERNAME')
DEFAULT_ADMIN_PASSWORD = secret_util.get_latest('TEST_DEFAULT_ADMIN_PASSWORD')