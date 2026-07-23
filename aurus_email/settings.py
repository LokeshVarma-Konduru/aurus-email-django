"""
Aurus AI - Django Email OTP Service
Settings with Gmail SMTP + CID embedded logo
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-aurus-dev-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# ─────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'otp_service',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aurus_email.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'otp_service' / 'templates'],
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

WSGI_APPLICATION = 'aurus_email.wsgi.application'

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE (SQLite for OTP storage)
# ─────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# EMAIL — Gmail SMTP with App Password
# ─────────────────────────────────────────────────────────────────────────────
EMAIL_BACKEND        = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST           = 'smtp.gmail.com'
EMAIL_PORT           = 587
EMAIL_USE_TLS        = True
EMAIL_HOST_USER      = config('EMAIL_HOST_USER',     default='loki1432varma@gmail.com')
EMAIL_HOST_PASSWORD  = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL   = config('DEFAULT_FROM_EMAIL',  default='Aurus AI <loki1432varma@gmail.com>')

# ─────────────────────────────────────────────────────────────────────────────
# OTP CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
OTP_EXPIRY_MINUTES = 10       # OTP expires after 10 minutes
OTP_LENGTH         = 6        # 6-digit OTP (like Aurus design)

# ─────────────────────────────────────────────────────────────────────────────
# LOGO PATHS (used in CID embedding)
# ─────────────────────────────────────────────────────────────────────────────
LOGO_DIR = BASE_DIR / 'otp_service' / 'static' / 'images'

# Map each logo variant — update filenames if yours differ
LOGOS = {
    'logo_black': LOGO_DIR / 'logo-black.jpeg',
    'logo_white': LOGO_DIR / 'logo-white.jpeg',
    'aurus_black': LOGO_DIR / 'aurus-black.jpeg',
    'aurus_white': LOGO_DIR / 'aurus-white.jpeg',
}

# Default logo used in OTP email (dark background → use white logo)
EMAIL_LOGO_KEY = 'aurus_white'

# ─────────────────────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ─────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/minute',       # Max 5 OTP requests per minute (anti-spam)
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# CORS (Allow frontend to call this API)
# ─────────────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True   # ← Restrict in production

# ─────────────────────────────────────────────────────────────────────────────
# STATIC FILES
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL    = '/static/'
STATIC_ROOT   = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'otp_service' / 'static']

# ─────────────────────────────────────────────────────────────────────────────
# MISC
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'       # IST
USE_TZ = True
