"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import datetime


load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '84cfffb5459f3daa4e9fa2f798a1edf4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'core',
    'user',
    'api',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LoginAttemptsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('DB_HOST'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'NAME': os.environ.get('DB_NAME'),
        'PORT': '3307',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Rescrevendo
STATIC_URL = 'static/static/'
# iMAGENS
MEDIA_URL = 'static/media/'

# Onde ficará as imagens
MEDIA_ROOT = 'vol/web/static/'
MEDIA_ROOT = 'vol/web/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modo de Autenticação
AUTH_USER_MODEL = 'core.User'

# Tornar não obrigatório colocar barra no final das rotas
APPEND_SLASH=False


CORS_ALLOW_ALL_ORIGINS = True #Permite qualquer dominio acessar api



REST_FRAMEWORK = {
    # Biblioteca de documentação
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Por padrão, todas rotas devem ter autenticação 
    'DEFAULT_PERMISSION_CLASSES': (
    #'rest_framework.permissions.IsAuthenticated',
    ),
    # Como é possível se autenticar
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # Autenticação base de sessões
        'rest_framework.authentication.SessionAuthentication',
        # Autenticação básica
        'rest_framework.authentication.BasicAuthentication',
        # Autenticação JWT
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

"""
Simple JWT fornece um backend de autenticação JSON Web Token para o Django REST Framework.
O objetivo é cobrir os casos de uso mais comuns de JWTs, oferecendo um conjunto conservador de recursos padrão
"""
SIMPLE_JWT = {
    #especifica por quanto tempo os tokens de acesso são válidos
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60),
    #objeto que especifica por quanto tempo os tokens de atualização são válidos, revalidar
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    # Forma para obter
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",

}


SPECTACULAR_SETTINGS = {
        'COMPONENT_SPLIT_REQUEST': True
}
