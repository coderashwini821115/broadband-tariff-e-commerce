"""
Development settings for broadband_platform project.
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Development-specific installed apps
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Internal IPs for debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Email backend for development - print emails to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable cache in development for testing
# Comment this out if you want to test caching locally
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Celery - Use eager mode in development (synchronous execution)
# Uncomment this to execute tasks synchronously for easier debugging
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True

# Add HTML renderer for development API browsing
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

# Extended JWT token lifetime for development
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=24)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=30)

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Logging - More verbose in development
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['apps']['level'] = 'DEBUG'

# Show SQL queries in console
LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}

# Debug toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

print(f"✓ Development settings loaded")
print(f"✓ Database: {DATABASES['default']['NAME']} @ {DATABASES['default']['HOST']}")
print(f"✓ Redis: {CACHES['default']['LOCATION']}")
print(f"✓ Celery Broker: {CELERY_BROKER_URL}")
