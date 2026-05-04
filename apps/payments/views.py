

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .services import PaymentService
from rest_framework.decorators import action
from .serializers import PaymentHistorySerializer, InitiatePaymentSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Payment
from ..subscriptions.models import Subscription
from drf_spectacular.utils import extend_schema

CustomUser = get_user_model()
class PaymentViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == CustomUser.RoleChoices.ADMIN:
            return Payment.objects.all()
        return Payment.objects.filter(user = self.request.user)

    def get_serializer_class(self):
        if self.action == 'initiate':
            return InitiatePaymentSerializer
        return PaymentHistorySerializer

    @extend_schema(request = InitiatePaymentSerializer)
    @action(detail = False, methods = ['post'])
    def initiate(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        try:
            # Pass the data to our Service Layer to do the heavy lifting!
            payment, razorpay_order= PaymentService.create_razorpay_order(
                user = request.user,
                subscription_id = serializer.validated_data['subscription_id']
            )
        except Subscription.DoesNotExist:
            return Response({
                "error": "Invalid subscription Id."
            }, status = status.HTTP_404_NOT_FOUND)

        # Return the HTTP Response
        return Response({
            "payment_id": payment.id,
            "razorpay_order_id": razorpay_order['id'],
            "amount": payment.amount,
            "currency": payment.currency
        })

    @action(detail = False, methods=['get'])
    def history(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)

class PaymentWebHookView(APIView):
    permission_classes = [AllowAny] #Critical: Razorpay isn't a logged in user

    def post(self, request):
        signature = request.headers.get('X-Razorpay-Signature')

        # We need the raw bytes for signature verification
        raw_body = request.body.decode('utf-8')

        try:
            PaymentService.verify_webhook(raw_body, signature)
            return Response({"status": "accepted"},
            status = status.HTTP_200_OK
            )
        except Exception as e:
            # We log the error but we can return 400 so Razorpay knows to retry if it's a real failure
            # like if the db operation failed
            return Response({"detail": str(e)}, status = 400)



