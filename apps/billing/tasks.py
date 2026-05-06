
from celery import shared_task
from .models import Invoice

@shared_task
def generate_invoice(user_id, payment_id, subscription_id, amount, currency, billing_period_start, billing_period_end):
    """
    Loosely coupled Celery task.
    Receives only primitive data — knows nothing about Payments or Subscriptions!
    """
    invoice = Invoice.objects.create(
        user_id=user_id,
        payment_id = payment_id,
        subscription_id = subscription_id,
        amount = amount,
        currency = currency,
        billing_period_start = billing_period_start,
        billing_period_end = billing_period_end
    )

    return str(invoice.invoice_number)