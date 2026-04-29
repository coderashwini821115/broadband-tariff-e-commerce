"""
Serializers for plans.
Will be implemented in Phase 3.
"""
from rest_framework import serializers
from .models import TariffPlan

class TariffPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffPlan
        fields = ['id', 'name', 'speed_mbps', 'data_limit_gb', 'price_monthly', 'price_annual', 'features', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
