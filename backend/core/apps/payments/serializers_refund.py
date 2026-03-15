from rest_framework import serializers
from .models import Refund


class RefundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Refund
        fields = [
            "id",
            "payment",
            "amount",
            "reason",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def validate(self, data):

        payment = data["payment"]
        amount = data["amount"]

        total_refunded = sum(r.amount for r in payment.refunds.all())

        if amount + total_refunded > payment.amount:
            raise serializers.ValidationError(
                "Refund exceeds payment amount"
            )

        return data