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

