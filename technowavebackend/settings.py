from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@rl&qm)2_!p1w0nx67!5(i&6sw)6qhbac(zilfy8fb46zmtpgc'

DEBUG = True

ALLOWED_HOSTS = ['evyvctpeuu.eu.loclx.io', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',

    'api',
    'products',
    'users',
    'configurators',
    'orders'
    
]

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173"
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


ROOT_URLCONF = 'technowavebackend.urls'

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

WSGI_APPLICATION = 'technowavebackend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '45monster23',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],

    'DEFAULT_PAGINATION_CLASS': [
        'rest_framework.pagination.PageNumberPagination',
    ],
    'PAGE_SIZE': 5,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


DJOSER = {
    'SERIALIZERS': {
        'user': 'users.serializers.CustomUserSerializer',
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'current_user': 'users.serializers.CustomUserSerializer'
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_list': ['rest_framework.permissions.IsAuthenticated']
    },
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False
}


SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
   'AUTH_HEADER_TYPES': ('Bearer',),
}
