import uuid
import secrets

from django.db import models

def generate_public_key() -> str:
    """
    Public key used by clients (safe to expose)
    """
    return "pk_" + secrets.token_hex(16)

def generate_secret_key() -> str:
    """
    Secret key used for server-to-server authentication
    Must NEVER be exposed publicly
    """
    return "sk_" + secrets.token_hex(32)

class Merchant(models.Model):

    class Scope(models.TextChoices):
        READ = "read", "Read only"
        WRITE = "write", "Write access"
        ADMIN = "admin", "Admin access"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    public_key = models.CharField(
        max_length=64,
        unique=True,
        default=generate_public_key,
        editable=False,
    )

    secret_key = models.CharField(
        max_length=128,
        unique=True,
        default=generate_secret_key,
        editable=False,
    )

    password = models.CharField(max_length=255)

    is_verified = models.BooleanField(default=False)

    verification_token = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    scope = models.CharField(
        max_length=10,
        choices=Scope.choices,
        default=Scope.ADMIN,
        help_text="Defines API access level"
    )

    is_active = models.BooleanField(default=True)

    webhook_url = models.URLField(
        blank=True,
        null=True,
        help_text="Webhook endpoint for payment notifications"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "merchants"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

    @property
    def is_authenticated(self):
        return True