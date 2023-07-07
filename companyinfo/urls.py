from django.urls import path
from .views import CompanyInfoListAPIView, CompanyInfoRetrieveUpdateDestroyAPIView, CompanyInfoCreateAPIView



urlpatterns = [
    path("", CompanyInfoListAPIView.as_view(), name="company-list"),
     path("create/", CompanyInfoCreateAPIView.as_view(), name="company-create"),
    path("<int:pk>/", CompanyInfoRetrieveUpdateDestroyAPIView.as_view(), name="company-retrieve-update-destroy")
]
