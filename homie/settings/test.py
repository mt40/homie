from homie.settings.local import *

"""
These settings is used by CI and App Engine Test. 
"""

print(f"base dir: {BASE_DIR}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '127.0.0.1',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'NAME': os.environ['DB_NAME'],
    }
}