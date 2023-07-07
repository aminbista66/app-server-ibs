from django.urls import path, include
from .views import (
    SupplierCreateAPIView,
    SupplierListAPIView,
    SupplierRetrieveUpdateDestroyAPIVIew
)


urlpatterns = [
    path("", SupplierListAPIView.as_view(), name="list-supplier"),
    path("create/", SupplierCreateAPIView.as_view(), name="create-supplier"),
    path("<int:pk>/", SupplierRetrieveUpdateDestroyAPIVIew.as_view(), name="retrieve-update-delete-supplier"),
    
    
    

]
urlpatterns = urlpatterns





