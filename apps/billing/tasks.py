from django.core.mail import send_mail
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

    # Fire invoice email as separate task (non-blocking)
    send_invoice_email.delay(str(invoice.id))

    return str(invoice.invoice_number)

@shared_task
def send_invoice_email(invoice_id):
    invoice = Invoice.objects.select_related('user').get(id = invoice_id)
    send_mail(
        subject=f"Your Invoice {invoice.invoice_number}",
        message=f"Hi {invoice.user.email},\n\nYour invoice {invoice.invoice_number} for ₹{invoice.amount} has been generated.\n\nThank you!",
        from_email="billing@broadband.com",
        recipient_list=[invoice.user.email],
        fail_silently=False,
    )