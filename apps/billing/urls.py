"""
URL patterns for billing.
Will be implemented in Phase 6.
"""
from .views import InvoiceViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'billing'

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename = 'invoice')

urlpatterns = router.urls
