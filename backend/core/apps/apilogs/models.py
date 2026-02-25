import uuid
from django.db import models


class APILog(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    merchant_id = models.UUIDField(
        null=True,
        blank=True
    )

    method = models.CharField(max_length=10)

    path = models.CharField(max_length=255)

    status_code = models.IntegerField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "api_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method} {self.path} {self.status_code}"