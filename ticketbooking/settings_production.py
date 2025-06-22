"""
Impostazioni di produzione per Railway
"""
import os
from .settings import *
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Security
DEBUG = False
ALLOWED_HOSTS = ['.up.railway.app', 'localhost', '127.0.0.1']

# Ottieni l'URL del dominio Railway
RAILWAY_STATIC_URL = os.getenv('RAILWAY_STATIC_URL', None)
if RAILWAY_STATIC_URL:
    ALLOWED_HOSTS.append(RAILWAY_STATIC_URL)

# CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://*.up.railway.app',
]

# Database - manteniamo SQLite anche in produzione
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/app/db.sqlite3',  # Percorso assoluto per Railway
    }
}

# Static files con WhiteNoise
# SUPPRIMÉ la ligne MIDDLEWARE.insert() car elle créait des doublons
# Le middleware WhiteNoise est déjà dans settings.py

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# IMPORTANTE: Usa CompressedStaticFilesStorage invece di CompressedManifestStaticFilesStorage
# per evitare errori con i file CSS dell'admin
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Cloudinary configuration
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

# SUPPRIMÉ - Ces lignes créaient des doublons car cloudinary est déjà dans settings.py
# INSTALLED_APPS.insert(0, 'cloudinary_storage')
# INSTALLED_APPS.insert(1, 'cloudinary')

# Media files su Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Disabilita la compressione WhiteNoise per i file dell'admin
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['map', 'css']