"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import os
from datetime import timedelta
import jwt

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG_VALUE', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # drf app
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.apple',
    'drf_yasg',
    'corsheaders',
    'social_django',

    # project app
    'accounts',
    'clinics',
    'todaylogs',
    'fastlogs',
    'news',
    'mypage',
    'notification',
    'magazine',
    'menstruation',
    'mail',
    'information',
    'community',
]

SITE_ID = 1
AUTH_USER_MODEL = 'accounts.User'

REST_USE_JWT = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # username 필드 사용 x
ACCOUNT_EMAIL_REQUIRED = True            # email 필드 사용 o
ACCOUNT_USERNAME_REQUIRED = False        # username 필드 사용 x
ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_VERIFICATION = 'none' # 회원가입 과정에서 이메일 인증 사용 X

REST_AUTH = {
    'USE_JWT' : True,
    'JWT_AUTH_HTTPONLY' : True,
    'JWT_AUTH_COOKIE' : "access_token",
    'JWT_AUTH_REFRESH_TOKEN' : "refresh_token",
    "JWT_AUTH_COOKIE_USE_CSRF" : True,
    'SESSION_LOGIN' : False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'accounts.authentication.KakaoAuthentication',
        'accounts.authentication.AppleAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_CHARSET': 'utf-8',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_KAKAO_KEY = config('SOCIAL_AUTH_KAKAO_KEY')
SOCIAL_AUTH_KAKAO_SECRET = config('SOCIAL_AUTH_KAKAO_SECRET', default='')
SOCIAL_AUTH_KAKAO_REDIRECT_URI = config('SOCIAL_AUTH_KAKAO_REDIRECT_URI')
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_USER_CLASS': "django.contrib.auth.models.User",
}

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': 'KAKAO_CLIENT_ID',
            'secret': 'KAKAO_SECRET_KEY',
            'key': 'KAKAO_REST_API_KEY',
        }
    },
    'apple': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_APPLE_CLIENT_ID'),
            'team_id': config('SOCIAL_AUTH_APPLE_TEAM_ID'),
            'key_id': config('SOCIAL_AUTH_APPLE_KEY_ID'),
            'private_key': config('SOCIAL_AUTH_APPLE_PRIVATE_KEY'),
            'redirect_uri': config('SOCIAL_AUTH_APPLE_REDIRECT_URI'),
        }
    },
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.kakao.KakaoOAuth2',
    'social_core.backends.apple.AppleIdAuth',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    #cors 설정
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# 기본 설정 (개발환경)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 배포환경에서의 설정
if config('DJANGO_DEPLOY', default=False, cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': config('DATABASE_ENGINE'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_USER_PASSWORD'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT')
        }
    }


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

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://www.neromakebrain.site', 'https://neromakebrain.site']
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.neromakebrain.site'
# corsheaders
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    # 로컬 개발용
    'http://localhost:3000',
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}