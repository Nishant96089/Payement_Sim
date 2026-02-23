from django.contrib import admin
from .models import Payment, IdempotencyKey


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "merchant",
        "amount",
        "currency",
        "status",
        "created_at",
    )

    list_filter = ("status", "currency")

    readonly_fields = ("id", "created_at", "updated_at")

@admin.register(IdempotencyKey)
class IdempotencyKeyAdmin(admin.ModelAdmin):

    list_display = (
        "key",
        "merchant",
        "payment",
        "created_at",
    )