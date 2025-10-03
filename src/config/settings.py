import os
from pathlib import Path
from dotenv import load_dotenv  

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# 🔑 Seguridad
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'DEV-ONLY-CHANGE-ME')
DEBUG = 'False'
ALLOWED_HOSTS = ['fede9420.pythonanywhere.com', 'www.fede9420.pythonanywhere.com']

# 📦 Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Extractor',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 🗄️ Base de datos (desde .env)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# 🔐 Validadores
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Argentina/Ushuaia'
USE_I18N = True
USE_TZ = True

# 📂 Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'Extractor' / 'static']

# 📂 Archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 🔑 Login
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'Extractor:login_view'
LOGIN_REDIRECT_URL = 'Extractor:extractor_view'
LOGOUT_REDIRECT_URL = 'Extractor:index'

# 🔌 N8N (BasicAuth)
N8N_USER = os.getenv("N8N_USER", "")
N8N_PASSWORD = os.getenv("N8N_PASSWORD", "")
N8N_URL = os.getenv("N8N_URL", "")
N8N_PULL_API_KEY = os.getenv("N8N_PULL_API_KEY", "")

# 👀 Config local (no obligatorio)
try:
    from .settings_dev import *
except ModuleNotFoundError:
    pass