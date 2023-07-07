from rest_framework import generics
from inventory.permissions.inventory_permissions import (
    CanChangeInventoryPermission,
    CanCreateInventoryPermission,
)
from invoice.filters.purchase_invoice_filters import PurchaseInvoiceFilter
from invoice.models.purchase_invoice import PurchaseInvoice
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from invoice.permissions.purchase_invoice_permissions import (
    CanCreatePurchaseInvoicePermission,
    CanViewPurchaseInvoicePermission,
)

from invoice.serializers.purchase_invoice_serializers import (
    PurchaseInvoiceCreateSerializer,
    PurchaseInvoiceSerializer,
)
from logs.logs_mixins import CustomCreateAPIView


class PurchaseInvoiceListAPIView(generics.ListAPIView):
    serializer_class = PurchaseInvoiceSerializer
    permission_classes = [CanViewPurchaseInvoicePermission]
    filterset_class = PurchaseInvoiceFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return PurchaseInvoice.objects.get_invoice_of_branch(
            branch, fiscal_year
        ).order_by("-created_at")


class PurchaseInvoiceCreateAPIView(CustomCreateAPIView):
    serializer_class = PurchaseInvoiceCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreatePurchaseInvoicePermission,
        CanCreateInventoryPermission,
        CanChangeInventoryPermission,
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return PurchaseInvoice.objects.get_invoice_of_branch(branch, fiscal_year).prefetch_related("purchase_invoice_line") 