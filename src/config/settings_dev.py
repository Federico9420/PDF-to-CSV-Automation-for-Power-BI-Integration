import os 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'extractor_db',
        'USER': 'FedericoJAlmonacid',
        'PASSWORD': 'F6e2d8e6!',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

