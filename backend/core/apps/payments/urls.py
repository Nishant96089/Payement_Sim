from django.urls import path
from .views import (
    PaymentCreateView,
    PaymentListView,
    PaymentDetailView,
    PaymentStatusUpdateView
)

urlpatterns = [
    path("", PaymentCreateView.as_view(), name="payment-create"),
    path("list/", PaymentListView.as_view(), name="payment-list"),
    path("<uuid:payment_id>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("<uuid:payment_id>/status/", PaymentStatusUpdateView.as_view(), name="payment-status-update"),

]