from homie.settings.local import *
from portfolio import secret_util

"""
These settings is used by CI and App Engine Test. 
"""

print(f"base dir: {BASE_DIR}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': secret_util.get_latest('TEST_DB_HOST'),
        'USER': secret_util.get_latest('TEST_DB_USER'),
        'PASSWORD': secret_util.get_latest('TEST_DB_PASSWORD'),
        'NAME': secret_util.get_latest('TEST_DB_NAME')
    }
}