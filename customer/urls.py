from django.urls import path
from .views import (
    CustomerListAPIView,
    CustomerCreateAPIView,
    CustomerRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path("", CustomerListAPIView.as_view(), name="customer-view"),
    path("create/", CustomerCreateAPIView.as_view(), name="customer-create"),
    path("<int:pk>/", CustomerRetrieveUpdateDeleteAPIView.as_view(), name="customer-retrieve-update-delete"),
]
