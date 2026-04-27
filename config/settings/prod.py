"""
Production settings for broadband_platform project.
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'api.broadband-platform.com').split(',')

# Security Settings for Production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# Session Security
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'

# CORS - Strict origins in production
CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOWED_ORIGINS should be set via environment variable

# Database - Production optimizations
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
    'options': '-c statement_timeout=30000',  # 30 second statement timeout
}

# Use AWS RDS SSL if available
if os.environ.get('DATABASE_URL_SSL'):
    DATABASES['default']['OPTIONS']['sslmode'] = 'require'

# Static files - Serve via CDN/S3 in production
# Uncomment and configure for AWS S3
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-south-1')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }

# Logging - Production configuration
LOGGING['handlers']['console']['level'] = 'WARNING'
LOGGING['handlers']['file']['level'] = 'ERROR'
LOGGING['loggers']['django']['level'] = 'WARNING'
LOGGING['loggers']['apps']['level'] = 'INFO'

# Add error email handler for production
LOGGING['handlers']['mail_admins'] = {
    'level': 'ERROR',
    'class': 'django.utils.log.AdminEmailHandler',
    'include_html': True,
}
LOGGING['loggers']['django']['handlers'].append('mail_admins')

# Admin notification emails
ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@broadband-platform.com')),
]
MANAGERS = ADMINS

# Email - Use production SMTP in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Performance - Optimize template rendering
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Celery - Production broker settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_POOL_LIMIT = 10

# Redis - Production cache settings
CACHES['default']['OPTIONS']['CONNECTION_POOL_KWARGS']['max_connections'] = 100

# REST Framework - Remove browsable API in production
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)

# Rate limiting (if using throttling)
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle'
]
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/hour',
    'user': '1000/hour'
}

print(f"✓ Production settings loaded")
print(f"✓ Allowed hosts: {ALLOWED_HOSTS}")
print(f"✓ Debug mode: {DEBUG}")
