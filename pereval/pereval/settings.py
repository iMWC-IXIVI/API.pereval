import os

from pathlib import Path

from dotenv import load_dotenv


load_dotenv()  # Загрузка переменных окружения

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')  # Ключ DJANGO

DEBUG = True

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]  # Список допустимых адресов

INSTALLED_APPS = [
    # Базовые приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Установленные приложения
    'rest_framework',

    'drf_spectacular',
    'drf_spectacular_sidecar',
    # Собственные приложения
    'pereval_app.apps.PerevalAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'pereval.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],  # Дирректория с шаблонами
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

WSGI_APPLICATION = 'pereval.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'NAME': os.getenv('NAME'),
        'PORT': os.getenv('PORT'),
    }
}  # Настройки базы данных в проекте postgresql

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

LANGUAGE_CODE = 'ru'  # Язык отображения

TIME_ZONE = 'Europe/Moscow'  # Часовой пояс

USE_I18N = True

USE_TZ = False

# Статик файлы
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# Медия файлы
MEDIA_ROOT = BASE_DIR/'images'
MEDIA_URL = 'images/'

# Настройки django-rest-framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

# Настройки spectacular (swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Pereval API',
    'DESCRIPTION': 'Special for FTSR - Pereval',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
}
