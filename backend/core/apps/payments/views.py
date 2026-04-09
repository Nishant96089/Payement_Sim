from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import PaymentCreateSerializer, PaymentStatusUpdateSerializer
from .models import Payment, IdempotencyKey, Refund
from .serializers import PaymentListSerializer
from .serializers_refund import RefundSerializer
from django.shortcuts import get_object_or_404
from .tasks import send_payment_webhook, process_payment
from apps.merchants.ratelimit import MerchantRateThrottle
from apps.payments.services.fraud_detection import evaluate_payment

@extend_schema(
    request=PaymentCreateSerializer,
    responses=PaymentCreateSerializer,
    description="Create a new payment (requires Idempotency-Key header)"
)
class PaymentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        MerchantRateThrottle().allow_request(request)

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
        payment.fraud_flag = evaluate_payment(payment)
        payment.save()
        payment.status = "processing"
        payment.save()
        process_payment.delay(str(payment.id))

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
    
@extend_schema(
    responses=PaymentListSerializer(many=True),
    description="List all payments for authenticated merchant"
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
    
@extend_schema(
    responses=PaymentListSerializer,
    description="Retrieve a specific payment"
)
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
    
@extend_schema(
    request=PaymentStatusUpdateSerializer,
    responses=OpenApiResponse(description="Payment status updated"),
    description="Update payment status and trigger webhook"
)
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
    
@extend_schema(
    request=RefundSerializer,
    responses=RefundSerializer,
    description="Create a refund for a payment"
)
class RefundCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = RefundSerializer(data=request.data)

        if serializer.is_valid():

            refund = serializer.save(
                merchant=request.user
            )

            return Response(
                RefundSerializer(refund).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)
    
@extend_schema(
    responses=RefundSerializer,
    description="Retrieve refund details"
)
class RefundDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, refund_id):

        refund = get_object_or_404(
            Refund,
            id=refund_id,
            merchant=request.user
        )

        return Response(
            RefundSerializer(refund).data
        )