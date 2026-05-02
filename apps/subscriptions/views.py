from .models import TariffPlan
from rest_framework.decorators import action
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from .models import Subscription
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscriptionSerializer
from drf_spectacular.utils import extend_schema, inline_serializer

CustomUser = get_user_model()
class SubscriptionViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SubscriptionSerializer

    # Security: No one can access subscriptions unless they have a valid JWT token
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Admins can see all subscriptions in the system.
        Normal customers can ONLY see their own subscriptions.
        """
        if self.request.user.role == CustomUser.RoleChoices.ADMIN:
            return Subscription.objects.all()

        return Subscription.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        """
        When a user POSTs to create a subscription, they don't send their User ID.
        We automatically attach their account to the subscription based on their JWT token!
        This way we make sure that a customer can only buy a plan for themselves
        """
        serializer.save(user = self.request.user)

    @extend_schema(request = inline_serializer(name = "CancelPlanRequest",
    fields = {}
    ))
    @action(detail = True, methods=['post'])    
    def cancel(self, request, pk=None):
        """
        Cancel a subscription.
        We don't delete the row; we just turn off auto-renew and set status to cancelled.
        """
        subscription = self.get_object()
        
        if subscription.status == Subscription.StatusChoices.CANCELLED:
            return Response({"detail": "Subscription is already cancelled"}, status = status.HTTP_400_BAD_REQUEST)

        subscription.status = Subscription.StatusChoices.CANCELLED
        subscription.auto_renew = False
        subscription.save()
        return Response(status = status.HTTP_204_NO_CONTENT)

    @extend_schema(request = None)
    @action(detail = True, methods=['post'])
    def upgrade(self, request, pk = None):
        """
        Upgrade to a different plan.
        Expects {"new_plan_id": "uuid"} in the request body.
        """
        subscription = self.get_object()
        new_plan_id = request.data.get('new_plan_id')

        if not new_plan_id:
            return Response({"error": "new_plan_id is required"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            new_plan = TariffPlan.objects.get(id = new_plan_id, is_active = True)
        except TariffPlan.DoesNotExist:
            return Response({"error": "invalid or inactive plan"}, status = status.HTTP_404_NOT_FOUND)

        # Update the plan
        subscription.plan = new_plan
        subscription.save()

        return Response({
            "detail": f"Successfully upgraded to {new_plan.name}!",
            "new_plan": new_plan.name
        })