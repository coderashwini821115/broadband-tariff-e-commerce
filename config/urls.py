"""
URL configuration for broadband_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 endpoints
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/plans/', include('apps.plans.urls')),
    path('api/v1/subscriptions/', include('apps.subscriptions.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Customize admin site
admin.site.site_header = 'Broadband B2C Platform Administration'
admin.site.site_title = 'Broadband Platform Admin'
admin.site.index_title = 'Welcome to Broadband Platform Admin'
