from django.core.cache import cache
from rest_framework.exceptions import Throttled

class MerchantRateThrottle:

    RATE_LIMIT = 100  # requests
    WINDOW = 60  # seconds

    def allow_request(self, request):

        merchant = request.user

        if not merchant or not merchant.is_authenticated:
            return True  # throttle only authenticated merchants
        
        key = f"ratelimit:{merchant.id}"

        current = cache.get(key, 0)

        if current >= self.RATE_LIMIT:
            raise Throttled(
                detail="Rate limit exceeded. Try again later.",
            )
        
        cache.set(
            key,
            current + 1,
            timeout=self.WINDOW
        )

        return True