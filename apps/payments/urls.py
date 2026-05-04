"""
URL patterns for payments.
Will be implemented in Phase 5.
"""
from .views import PaymentWebHookView
from django.urls import include
from .views import PaymentViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'payments'

router = DefaultRouter()
router.register('', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', PaymentWebHookView.as_view(), name = 'webhook'),
]
