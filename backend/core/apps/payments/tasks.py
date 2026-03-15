import random
import time
import requests
from celery import shared_task
from .models import Payment


@shared_task
def send_payment_webhook(webhook_url, payload):

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=5
        )

        return response.status_code

    except Exception as e:
        return str(e)
    
@shared_task
def process_payment(payment_id):

    time.sleep(5)  # simulate processing delay

    payment = Payment.objects.get(id=payment_id)

    if payment.fraud_flag:
        payment.status = "failed"
    else:
        payment.status = random.choice(["success", "failed"])

    payment.save()

    merchant = payment.merchant

    if merchant.webhook_url:

        payload = {
            "event": f"payment.{payment.status}",
            "payment_id": str(payment.id),
            "status": payment.status,
            "amount": payment.amount,
        }

        send_payment_webhook.delay(
            merchant.webhook_url,
            payload
        )
