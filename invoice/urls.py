from django.urls import path

from invoice.views.purchase_invoice_views import (
    PurchaseInvoiceCreateAPIView,
    PurchaseInvoiceListAPIView,
)

from invoice.views.purchase_invoice_image_views import (
    PurchaseInvoiceImageCreateAPIView,
    PurchaseInvoiceImageRetrieveDeleteAPIView
)

urlpatterns = [
    path(
        "purchases/", PurchaseInvoiceListAPIView.as_view(), name="purchase_invoice_list"
    ),
    path(
        "purchases/create/",
        PurchaseInvoiceCreateAPIView.as_view(),
        name="purchase_invoice_create",
    ),
    path(
        "purchases/images/create/",
        PurchaseInvoiceImageCreateAPIView.as_view(),
        name="purchase_invoice_image_create",
    ),
    path("purchases/images/<int:pk>/",
         PurchaseInvoiceImageRetrieveDeleteAPIView.as_view(),
         name="purchase_invoice_image_retrieve_delete")
]
