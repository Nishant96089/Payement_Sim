from .models import APILog


class APILogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        merchant_id = None

        if hasattr(request, "user") and request.user:
            merchant_id = getattr(request.user, "id", None)

        ip = request.META.get("REMOTE_ADDR")

        APILog.objects.create(
            merchant_id=merchant_id,
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            ip_address=ip,
        )

        return response