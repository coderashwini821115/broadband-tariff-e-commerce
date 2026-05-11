from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'subscription_id',
            'payment_id',
            'amount',
            'currency',
            'billing_period_start',
            'billing_period_end',
            'ai_summary',
            'created_at'
        ]
        read_only_fields = fields