import os
from google.cloud import secretmanager

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()

projectId = '583793981505'

secretSecretKeyId = str(os.environ.get('secretSecretKeyId'))
BBPassword = client.access_secret_version(request = {
    "name": 'projects/' + projectId + '/secrets/DBPassword/versions/1'}) \
    .payload.data.decode("UTF-8")
DBUser = client.access_secret_version(request = {
    'name': 'projects/' + projectId + '/secrets/DBUser/versions/1'}) \
    .payload.data.decode("UTF-8")
DBName = client.access_secret_version(request = {
    "name": 'projects/' + projectId + '/secrets/DBName/versions/1'}) \
    .payload.data.decode("UTF-8")
DBHost = client.access_secret_version(request = {
    "name": 'projects/' + projectId + '/secrets/DBHost/versions/1'}) \
    .payload.data.decode("UTF-8")
DBEngine = client.access_secret_version(request = {
    "name": 'projects/' + projectId + '/secrets/DBEngine/versions/1'}) \
    .payload.data.decode("UTF-8")
SECRET_KEY = client.access_secret_version(request = {
    "name": 'projects/' + projectId + '/secrets/SecretKey/versions/1'}) \
    .payload.data.decode("UTF-8")

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'crispy_forms',
    'django_countries',

    'core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'djecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djecommerce.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Costa_Rica'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'https://storage.googleapis.com/test3363/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

# Auth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# CRISPY FORMS

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# gmail_send/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = client.access_secret_version(request = {
    "name": 'projects/' + projectId + '/secrets/EmailUser/versions/1'}) \
    .payload.data.decode("UTF-8")
EMAIL_HOST_PASSWORD = client.access_secret_version(request = {
    'name': 'projects/' + projectId + '/secrets/EmailPassword/versions/1'}) \
    .payload.data.decode("UTF-8")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
