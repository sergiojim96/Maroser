from .base import *

DEBUG = False
ALLOWED_HOSTS = ['test3363.uc.r.appspot.com']

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database2',
        'USER': 'usuario2',
        'PASSWORD': 'holamundo',
        'HOST': '/cloudsql/test3363:us-central1:instancia2',
    }
}