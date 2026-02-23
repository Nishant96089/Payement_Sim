from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import MerchantSerializer


class MerchantMeView(APIView):
    """
    Return currently authenticated merchant
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        merchant = request.user
        serializer = MerchantSerializer(merchant)

        return Response(serializer.data)