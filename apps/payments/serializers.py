from rest_framework import serializers
from .models import Payment

class InitiatePaymentSerializer(serializers.Serializer):
    subscription_id = serializers.UUIDField()
    # We will look up the price securely in the backend, 
    # so we DO NOT accept 'amount' from the frontend!

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'subscription_id', 'amount', 'currency', 'status', 'gateway', 'created_at']
        read_only_fields = fields