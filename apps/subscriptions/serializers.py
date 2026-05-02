
from django.utils import timezone
from datetime import timedelta
from ..plans.serializers import TariffPlanSerializer
from rest_framework import serializers
from .models import Subscription
class SubscriptionSerializer(serializers.ModelSerializer):
    # When fetching subscriptions, we want to see the full Plan JSON, not just a raw UUID
    plan_details = TariffPlanSerializer(source = 'plan', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_details', 'status', 'billing_cycle', 'start_date', 'end_date', 'auto_renew', 'created_at']
        read_only_fields = ['id', 'status', 'start_date', 'end_date', 'created_at']

    def validate(self, data):
        plan = data.get('plan')
        if plan and not plan.is_active:
            raise serializers.ValidationError({"plan": "This plan is currently inactive and cannot be purchased"})
        
        return data

    def create(self, validated_data):
        billing_cycle = validated_data.get('billing_cycle')
        start_date = timezone.now()

        if billing_cycle == Subscription.BillingCycleChoices.MONTHLY:
            end_date = start_date + timedelta(days = 30)
        else:
            end_date = start_date + timedelta(days = 365)

        validated_data['start_date'] = start_date
        validated_data['end_date'] = end_date

        return super().create(validated_data)