from django.db import transaction
import json
from ..subscriptions.models import Subscription
from django.conf import settings
import razorpay
import hashlib
from .models import Payment
from datetime import datetime

class PaymentService:
    @staticmethod
    def create_razorpay_order(user, subscription_id):
        """
        Pure business logic. No HTTP Requests or Responses here!
        """
        # 1. Generate the SHA-256 Idempotency key
        today = datetime.now().strftime('%Y-%m-%d')
        raw_string = f'{user.id}-{subscription_id}-{today}'
        idem_key = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

        # 2. Idempotency check: did they already click pay today?
        existing_payment = Payment.objects.filter(idempotency_key=idem_key).first()

        if existing_payment:
            return existing_payment, {"id": existing_payment.gateway_order_id}

        # 3. Initialize Razorpay
        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # 4. Fetch the subscription (Will raise DoesNotExist if invalid, which the view will catch)
        subscription = Subscription.objects.get(id = subscription_id, user = user, status = Subscription.StatusChoices.PENDING)

        # 5. Calculate amount
        amount = subscription.plan.price_monthly if subscription.billing_cycle == 'monthly' else subscription.plan.price_annual
        
        # since razorpay only accepts amount in paise
        amount_in_paise = int(amount*100)

        # 6. call razorpay api
        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"rcpt_{subscription.id.hex[:10]}"
        })

        # 7. Save the pending payment to our database
        payment = Payment.objects.create(
            user = user,
            subscription_id = subscription.id,
            amount = amount,
            currency = "INR",
            gateway = 'razorpay',
            gateway_order_id = razorpay_order['id'],
            idempotency_key = idem_key,
            status = Payment.StatusChoices.PENDING
        )
        return payment, razorpay_order

    @staticmethod
    def verify_webhook(raw_body, signature):
        """
        1. Verifies the cryptographic signature to ensure it's actually Razorpay.
        2. Updates Payment to SUCCESS.
        3. Updates Subscription to ACTIVE.
        """
        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # 1. SECURITY: Verify the signature
        try:
            # we must use raw string body, not a parsed dictionary!
            client.utility.verify_webhook_signature(
                raw_body,
                signature,
                settings.RAZORPAY_WEBHOOK_SECRET
            )
        except razorpay.errors.SignatureVerificationError:
            raise ValueError("invalid signature: hack attempt blocked")

        # 2. Parse the JSON now that we know it's safe
        payload = json.loads(raw_body)
        event_type = payload.get('event')

        # we only care when the orderr is successfully paid
        if event_type == 'order.paid':
            payment_entity = payload['payload']['payment']['entity']
            razorpay_order_id = payment_entity['order_id']
            razorpay_payment_id = payment_entity['id']

            # 3. DISTRIBUTED TRANSACTION: Update Payment & Subscription together
            with transaction.atomic():
                # # select_for_update() locks the row so no other request can modify it right now
                payment = Payment.objects.select_for_update().get(gateway_order_id = razorpay_order_id)

                if payment.status != Payment.StatusChoices.SUCCESS:
                    # Update Payment
                    payment.status = Payment.StatusChoices.SUCCESS
                    payment.gateway_payment_id = razorpay_payment_id
                    payment.metadata = payload #dump the whole json here for debugging
                    payment.save()

                    # Activate Subscription
                    subscription = Subscription.objects.get(id = payment.subscription_id)
                    subscription.status = Subscription.StatusChoices.ACTIVE
                    subscription.save()

        return True