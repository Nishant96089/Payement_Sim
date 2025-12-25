from django.contrib import admin
from .models import Merchant

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "name",
        "email",
        "public_key",
        "is_active",
        "created_at",
    )

    list_filter=("is_active", "created_at")
    search_fields=("name", "email", "public_key")

    readonly_fields=(
        "id",
        "public_key",
        "secret_key",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
