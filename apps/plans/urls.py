"""
URL patterns for plans.
Will be implemented in Phase 3.
"""
from .views import TariffPlanViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'plans'

router = DefaultRouter()
# Note: we use an empty string '' because in config/urls.py we already mapped 'api/v1/plans/' to this file.
router.register('', TariffPlanViewSet, basename='plans')

urlpatterns = [
    # Will be implemented in Phase 3
]
urlpatterns += router.urls
