import uuid
from django.db import models

from apps.merchants.models import Merchant


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    class Currency(models.TextChoices):
        INR = "INR", "Indian Rupee"
        USD = "USD", "US Dollar"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.PositiveIntegerField(
        help_text="Amount in smallest currency unit (paise, cents)"
    )

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.INR,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    fraud_flag = models.BooleanField(
        default=False,
        help_text="Marks suspicious payments detected by Payment engine"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} - {self.amount} {self.currency}"
    
class IdempotencyKey(models.Model):

    key = models.CharField(
        max_length=255,
        unique=True
    )

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE
    )

    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "idempotency_keys"

    def __str__(self):
        return self.key
    
class Refund(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="refunds",
    )

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField(
        help_text="Refund amount in smallest currency unit"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "refunds"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Refund {self.id}"