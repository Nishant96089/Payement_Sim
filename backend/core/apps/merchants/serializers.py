import secrets
from rest_framework import serializers
from .models import Merchant
from .utils import hash_password


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id",
            "name",
            "email",
            "public_key",
            "created_at",
        ]


class MerchantRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Merchant
        fields = [
            "name",
            "email",
            "password",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        merchant = Merchant.objects.create(
            **validated_data,
            password=hash_password(password),
            verification_token=secrets.token_hex(32)
        )

        return merchant