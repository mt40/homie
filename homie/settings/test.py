from homie.settings.local import *

"""
These settings is used by CI and App Engine Test. 
"""

print(f"base dir: {BASE_DIR}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': f'/cloudsql/{os.environ["CLOUD_SQL_CONNECTION_NAME"]}',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'NAME': os.environ['DB_NAME'],
    }
}