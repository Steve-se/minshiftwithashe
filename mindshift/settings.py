
from pathlib import Path
import os
import logging
import environ
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR/'templates'

env = environ.Env()
environ.Env.read_env(os.path.join('.env'))

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['mindshiftwithashe.onrender.com', 'www.mindshiftwithashe.com', 'mindshiftwithashe.com', 'localhost:8000']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # local
    
    'blog',

    'author',
    'pledge',
    'newsletter',
    
    # dependencies 
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mindshift.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'mindshift.wsgi.application'

# CONFIGURING DJANGO MAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mindshiftwithashe@gmail.com'
EMAIL_HOST_PASSWORD = 'bshy xgff tjpy tnzi'
EMAIL_PORT = '465'
# EMAIL_USE_TLS = 'True'
EMAIL_USE_SSL = 'True'




# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# DATABASES= {'default': dj_database_url.parse(env('DATABASE_URL'))}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


CKEDITOR_UPLOAD_PATH = "uploads/"

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# WhiteNoise specific settings
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use HTTPS everywhere
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS

# HSTS (forces browsers to use HTTPS only)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies (prevent leakage over HTTP)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent browser from guessing content type (security hardening)
SECURE_CONTENT_TYPE_NOSNIFF = True

# Prevent your site from being iframed (mitigate clickjacking)
X_FRAME_OPTIONS = "DENY"

# Use modern referrer policy
SECURE_REFERRER_POLICY = "strict-origin"

# Set default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


logging.basicConfig(
    filename='Mindshift.log',
    filemode='a',
    level=logging.DEBUG,
    format='[{asctime}] {levelname} {module} {thread:d} - {message}',
    datefmt='%d-%m-%Y %H:%M:%S',
    style='{',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {module} {thread:d} - {message}',
            'style': '{',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'Mindshift.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.response': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

