from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Merchant
from .serializers import MerchantSerializer, MerchantRegisterSerializer

@extend_schema(
    responses=MerchantSerializer,
    description="Get currently authenticated merchant"
)
class MerchantMeView(APIView):
    """
    Return currently authenticated merchant
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        merchant = request.user
        serializer = MerchantSerializer(merchant)

        return Response(serializer.data)
    
@extend_schema(
    request=MerchantRegisterSerializer,
    responses=OpenApiResponse(description="Merchant registered successfully"),
    description="Register a new merchant"
)
class MerchantRegisterView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = MerchantRegisterSerializer(data=request.data)

        if serializer.is_valid():

            merchant = serializer.save()

            return Response({
                "message": "Merchant registered successfully",
                "verification_token": merchant.verification_token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(
    description="Verify merchant account using token"
)
class MerchantVerifyView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        token = request.data.get("token")

        merchant = get_object_or_404(
            Merchant,
            verification_token=token
        )

        merchant.is_verified = True
        merchant.verification_token = None
        merchant.save()

        return Response({
            "message": "Account verified successfully"
        })
    
@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
            }
        }
    },
    responses=OpenApiResponse(description="Returns API keys"),
    description="Login merchant and return API keys"
)
class MerchantLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        merchant = Merchant.objects.filter(email=email).first()

        if not merchant:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, merchant.password):
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not merchant.is_verified:
            return Response(
                {"error": "Account not verified"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "merchant_id": merchant.id,
            "public_key": merchant.public_key,
            "secret_key": merchant.secret_key
        })