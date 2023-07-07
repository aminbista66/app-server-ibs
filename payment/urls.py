from django.urls import path
from .views import (
    PaymentMethodListAPIView,
    PaymentMethodCreateAPIView,
    PaymentMethodRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path(
        "methods/",
        PaymentMethodListAPIView.as_view(),
        name="paymentmethod.list"
    ),
    path(
        "methods/create/",
        PaymentMethodCreateAPIView.as_view(),
        name="paymentmethod.create"
    ),
    path(
        "methods/<int:pk>/",
        PaymentMethodRetrieveUpdateDeleteAPIView.as_view(),
        name="paymentmethod.retrieve-update-delete"
    )
]
