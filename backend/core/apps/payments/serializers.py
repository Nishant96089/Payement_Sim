from rest_framework import serializers
from .models import Payment


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ["id", "amount", "currency", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    def create(self, validated_data):
        merchant = self.context["request"].user

        return Payment.objects.create(
            merchant=merchant,
            **validated_data
        )
    
class PaymentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "currency",
            "status",
            "created_at",
        ]

class PaymentStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ["status"]

    def validate_status(self, value):

        allowed = ["success", "failed"]

        if value not in allowed:
            raise serializers.ValidationError(
                "Status must be 'success' or 'failed'"
            )

        return value