from django.urls import path
from .views import MerchantMeView, MerchantRegisterView, MerchantVerifyView, MerchantLoginView

urlpatterns = [
    path("me/", MerchantMeView.as_view(), name="merchant-me"),
    path("register/", MerchantRegisterView.as_view()),
    path("verify/", MerchantVerifyView.as_view()),
    path("login/", MerchantLoginView.as_view()),
]