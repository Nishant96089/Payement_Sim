from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Merchant


class MerchantSecretKeyAuthentication(BaseAuthentication):
    """
    Authenticate merchant using secret key from Authorization header

    Expected header format:
        Authorization: Bearer sk_xxxxxxxxxxxxxxxxx
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # No auth provided

        try:
            keyword, secret_key = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        if keyword != self.keyword:
            raise AuthenticationFailed("Invalid authentication scheme")

        try:
            merchant = Merchant.objects.get(secret_key=secret_key)
        except Merchant.DoesNotExist:
            raise AuthenticationFailed("Invalid secret key")

        if not merchant.is_active:
            raise AuthenticationFailed("Merchant account is inactive")

        # Attach merchant to request
        return (merchant, None)