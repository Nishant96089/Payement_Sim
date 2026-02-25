from django.contrib import admin
from .models import APILog

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):

    list_display = (
        "method",
        "path",
        "status_code",
        "merchant_id",
        "created_at",
    )

    readonly_fields = (
        "merchant_id",
        "method",
        "path",
        "status_code",
        "ip_address",
        "created_at",
    )
