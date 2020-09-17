import os
from decouple import config
import django_heroku
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY',cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS',cast=list, default=['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ariadne.contrib.django',
    'corsheaders',
    'apps.auth_jwt',
    'apps.account',
    'apps.form',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_USER_MODEL = "account.CustomUser"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
     'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
  "apps.auth_jwt.backends.JSONWebTokenBackend",
  "django.contrib.auth.backends.ModelBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#CORS_ORIGIN_ALLOW_ALL=True
CORS_ORIGIN_WHITELIST = ["http://localhost:3000","http://localhost:8000","http://127.0.0.1:8000"]
CORS_ORIGIN_WHITELIST.append(config('FRONTEND_URL',cast=str))
CORS_ORIGIN_WHITELIST.append(config('DASHBOARD_URL',cast=str))
CORS_ALLOW_CREDENTIALS=True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

CSRF_TRUSTED_ORIGINS =['localhost:3000','app.deform.ujjawal.co','deform.ujjawal.co']
CSRF_TRUSTED_ORIGINS.append(config('FRONTEND_URL',cast=str))
CSRF_TRUSTED_ORIGINS.append(config('DASHBOARD_URL',cast=str))


CELERY_BROKER_URL = config('CELERY_BROKER_URL',cast=str)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER='json'
django_heroku.settings(locals())