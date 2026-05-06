"""
Models for billing and invoices.
Will be implemented in Phase 6.
"""
import uuid
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Invoice(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='invoices')

    subscription_id = models.UUIDField()
    payment_id = models.UUIDField()

    # Auto-generated human-readable invoice number e.g. INV-2026-00001
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length = 3, default = 'INR')
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()

    # LLM-generated summary (Phase 8)
    ai_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        # Auto-generate invoice number on first save
        if not self.invoice_number:
            from datetime import datetime
            year = datetime.now().year
            count = Invoice.objects.filter(created_at__year = year).count()+1
            self.invoice_number = f"INV-{year}-{count:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.user.email}"