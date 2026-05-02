"""
Views for plans.
Will be implemented in Phase 3.
"""
from rest_framework.decorators import action
from rest_framework.response import Response
from ..users.permissions import IsAdminRole
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import TariffPlanSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .models import TariffPlan


class TariffPlanViewSet(ModelViewSet):
    serializer_class = TariffPlanSerializer

    def get_permissions(self):
        # Anyone (even non-logged-in visitors) can view the plans catalogue
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        # Authenticated users can ask AI for recommendations
        if self.action == 'recommend':
            return [IsAuthenticated()]
        
        # Only Admins can CREATE, UPDATE, or DELETE plans
        return [IsAdminRole()]

    def get_queryset(self):
        """
        Admins should see ALL plans (including inactive/draft ones).
        Customers should ONLY see active plans.
        """
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return TariffPlan.objects.all()

        return TariffPlan.objects.filter(is_active = True)

    @action(detail=False, methods=['get'])
    def recommend(self, request):
        """
        AI Plan Recommendation endpoint. 
        We will wire up the Claude API logic here in Phase 8.
        """
        return Response({"message": "AI Plan recommendation will be built in Phase 8!"})

    # CACHING LOGIC
    def list(self, request, *args, **kwargs):
        # we only cache the standard user view, Admins get live Db data
        if request.user.is_authenticated and request.user.role == 'admin':
            return super().list(request, *args, **kwargs)

        cache_key = 'plans:active'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            print('cache hit , serving data')
            return Response(cached_data)

        # if not in cache, fetch from db
        response = super().list(request, *args, **kwargs)

        # cache for 1 hour (3600 seconds)
        cache.set(cache_key, response.data, 3600)
        return response

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return super().retrieve(request, *args, **kwargs)

        plan_id = kwargs.get('pk')
        cache_key = f'plan:{plan_id}'
        cache_data = cache.get(cache_key)

        if cache_data is not None:
            return Response(cache_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, 3600)
        return response

    # CACHE INVALIDATION
    def clear_cache(self, instance=None):
        # helper to clear plan caches when data changes
        cache.delete('plans:active')
        if instance:
            cache.delete(f'plan:{instance.id}')

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.clear_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.clear_cache(serializer.instance)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.clear_cache(instance)

