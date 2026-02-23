from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import PaymentCreateSerializer, PaymentStatusUpdateSerializer
from .models import Payment, IdempotencyKey
from .serializers import PaymentListSerializer
from django.shortcuts import get_object_or_404
from .tasks import send_payment_webhook


class PaymentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        merchant = request.user

        idempotency_key = request.headers.get("Idempotency-Key")

        if not idempotency_key:
            return Response(
                {"error": "Idempotency-Key header required"},
                status=400
            )

        # Check existing key
        existing = IdempotencyKey.objects.filter(
            key=idempotency_key,
            merchant=merchant
        ).first()

        if existing:
            serializer = PaymentCreateSerializer(existing.payment)
            return Response(serializer.data)

        # Create new payment
        serializer = PaymentCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        payment = serializer.save()

        # Store idempotency key
        IdempotencyKey.objects.create(
            key=idempotency_key,
            merchant=merchant,
            payment=payment
        )

        return Response(
            PaymentCreateSerializer(payment).data,
            status=201
        )
    
class PaymentListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        merchant = request.user

        payments = Payment.objects.filter(
            merchant=merchant
        ).order_by("-created_at")

        serializer = PaymentListSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)    
    
class PaymentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):

        merchant = request.user

        payment = get_object_or_404(
            Payment,
            id=payment_id,
            merchant=merchant
        )

        serializer = PaymentListSerializer(payment)

        return Response(serializer.data)
    
class PaymentStatusUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, payment_id):

        merchant = request.user

        payment = get_object_or_404(
            Payment,
            id=payment_id,
            merchant=merchant
        )

        serializer = PaymentStatusUpdateSerializer(
            payment,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        # Send webhook if configured
        if merchant.webhook_url:

            payload = {
                "event": f"payment.{payment.status}",
                "payment_id": str(payment.id),
                "amount": payment.amount,
                "currency": payment.currency,
                "status": payment.status,
            }

            send_payment_webhook.delay(
                merchant.webhook_url,
                payload
            )

        return Response({
            "id": str(payment.id),
            "status": payment.status
        })