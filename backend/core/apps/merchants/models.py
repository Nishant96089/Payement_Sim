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
    """
    Represents a business using the payment gateway
    """

    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)

    public_key=models.CharField(
        max_length=64,
        unique=True,
        default=generate_public_key,
        editable=False,
    )

    secret_key=models.CharField(
        max_length=128,
        unique=True,
        default=generate_secret_key,
        editable=False,
    )

    is_active=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="merchants"
        ordering=["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

