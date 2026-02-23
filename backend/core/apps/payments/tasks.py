import requests
from celery import shared_task


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