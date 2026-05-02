"""
URL patterns for subscriptions.
Will be implemented in Phase 4.
"""
from .views import SubscriptionViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    # Will be implemented in Phase 4
    path('', include(router.urls))
]
