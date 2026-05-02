"""
Models for subscriptions.
Will be implemented in Phase 4.
"""
from django.utils import timezone
from ..plans.models import TariffPlan
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.db import models

User = get_user_model()
class Subscription(models.Model):
    #Generic Subscription model. Highly flexible to support broadband, energy, or standard SaaS.
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        EXPIRED = 'expired', 'Expired'
        CANCELLED = 'cancelled', 'Cancelled'
        PENDING = 'pending ', 'Pending'

    class BillingCycleChoices(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    id = models.UUIDField(primary_key=True, default = uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(TariffPlan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length = 20, choices = StatusChoices.choices, default = StatusChoices.PENDING)
    billing_cycle = models.CharField(max_length = 20, choices = BillingCycleChoices.choices, default = BillingCycleChoices.ANNUAL)
    start_date = models.DateTimeField(default = timezone.now)
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            # Highly optimizes `GET /api/v1/subscriptions/` which filters by user and status.
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} - {self.status}"
