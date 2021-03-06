"""
Django settings for useless_mutant_project project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = [("James", 'wantsomechocolate@gmail.com')]
MANAGERS = [("James", 'wantsomechocolate@gmail.com')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['BOTD_DJANGO_SECRETKEY']


# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['BOTD_DJANGO_DEBUG']=="True":
    DEBUG = True
else:
    DEBUG = False

## ALLOWED HOSTS!
allowed_host_text = os.environ['BOTD_DJANGO_ALLOWEDHOSTS'] 
ALLOWED_HOSTS = []
for item in allowed_host_text.split(","):
    ALLOWED_HOSTS.append(item.strip())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Apps
    'useless_mutant',

    # Third Party Apps
    'storages',
    #'django_celery_results',
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

ROOT_URLCONF = 'useless_mutant_project.urls'

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

WSGI_APPLICATION = 'useless_mutant_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
from urllib.parse import urlparse
DB_INFO = urlparse(os.environ['BOTD_HEROKU_POSTGRESDB'])

DATABASES = {
    'default': {
        'ENGINE'    :   'django.db.backends.postgresql' ,
        'NAME'      :   DB_INFO.path[1:]               ,                      
        'USER'      :   DB_INFO.username                ,
        'PASSWORD'  :   DB_INFO.password                ,
        'HOST'      :   DB_INFO.hostname                ,
        #'PORT'      :   DB_INFO.port                    ,
    },


    'local': {
        'ENGINE'    :   'django.db.backends.sqlite3'            ,
        'NAME'      :   os.path.join(BASE_DIR, 'db.sqlite3')    ,
        'USER'      :   ''                                      ,
        'PASSWORD'  :   ''                                      ,
        'HOST'      :   ''                                      ,
        'PORT'      :   ''                                      ,
    }




}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
#TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

MEDIA_ROOT  =   os.path.join(BASE_DIR,  'media')
MEDIA_URL   =   '/media/'

STATIC_ROOT =   os.path.join(BASE_DIR,  'static')
STATIC_URL  =   '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]


## Added as part of real python tutorial

## Added for Celery
#CELERY_RESULT_BACKEND = 'django-db'


## For S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ['BOTD_AWS_ACCESSKEY']
AWS_SECRET_ACCESS_KEY = os.environ['BOTD_AWS_SECRETKEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BOTD_AWS_BUCKETNAME']
AWS_S3_REGION_NAME = "us-west-2"
AWS_DEFAULT_ACL = None

## FOR EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['BOTD_DJANGO_EMAILHOSTUSER']
EMAIL_HOST_PASSWORD = os.environ['BOTD_DJANGO_EMAILHOSTPASSWORD']

## Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'botd.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#         'MYAPP': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     }
# }





django_heroku.settings(locals())