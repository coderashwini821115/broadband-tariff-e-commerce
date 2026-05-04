"""
Models for payments.
Will be implemented in Phase 5.
"""
import uuid
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name = 'payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length = 3, default = 'INR')
    status = models.CharField(max_length = 20, choices = StatusChoices.choices, default = StatusChoices.PENDING)

    # The database doesn't know what a 'Subscription' is, so they are fully decoupled! (client will send this sub_id)
    subscription_id = models.UUIDField()

    # E.g: stripe or Razorpay
    gateway = models.CharField(max_length = 50)

    # Razorpay 'order_xxx' or Stripe 'pi_xxx' (Created before payment)
    gateway_order_id = models.CharField(max_length = 255, null = True, blank = True)

    # Razorpay 'pay_xxx' or Stripe 'ch_xxx' (Created after successful payment)
    gateway_payment_id = models.CharField(max_length = 255, unique = True, blank = True)

    # Prevents double-charging if the user double-clicks the Pay button
    idempotency_key = models.CharField(max_length = 255, unique = True)

    # --- PRODUCTION STANDARD ---
    # We will dump the raw Razorpay webhook JSON here so you can debug failed payments later.
    metadata = models.JSONField(default=dict, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['idempotency_key']),
            models.Index(fields = ['gateway_payment_id']),
            models.Index(fields=['subscription_id']),
        ]

    def __str__(self):
        return f'{self.user.email} - {self.amount} {self.currency} - {self.status}'


