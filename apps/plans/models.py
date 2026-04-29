"""
Models for tariff plans.
Will be implemented in Phase 3.
"""
import uuid
from django.db import models
from django.db.models import Q

class TariffPlan(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(unique = True, help_text = "e.g., Basic, Standard, Premium")
    speed_mbps = models.IntegerField(help_text="Download speed in Mbps")
    data_limit_gb = models.IntegerField(null=True, blank = True, help_text="Data limit in GB. Leave blank for unlimited.")
    price_monthly = models.DecimalField(max_digits=8, decimal_places=2)
    price_annual = models.DecimalField(max_digits=8, decimal_places=2)
    features = models.JSONField(default = list, blank = True)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.speed_mbps}Mbps"
    class Meta: 
        indexes = [
            models.Index(
                fields=['is_active'],
                condition = Q(is_active=True),
                name = 'idx_active_plans'
            )
        ]