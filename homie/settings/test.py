from google.auth.exceptions import DefaultCredentialsError

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


# automatically log out after a short time (in seconds)
SESSION_COOKIE_AGE = 60 * 60


try:
    from google.cloud import logging
    # Instantiates a client
    client = logging.Client()
    # Connects the logger to the root logging handler; by default
    # this captures all logs at INFO level and higher
    client.setup_logging()

    LOGGING = {
        'version': 1,
        'handlers': {
            'cloud_logging': {
                'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
                'client': client
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['cloud_logging'],
                'level': 'INFO',
                'name': 'test_app',
                'propagate': True
            }
        },
    }
except DefaultCredentialsError as error:
    print(str(error))