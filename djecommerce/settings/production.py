from .base import *


DEBUG = False
ALLOWED_HOSTS = ['209.97.157.199', '127.0.0.1', 'localhost', 'sashashop.cr', 'www.sashashop.cr']

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sasha',
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': '',
        'PORT': '',
    }
}
