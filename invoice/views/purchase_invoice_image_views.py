from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from invoice.models.purchase_invoice_image import PurchaseInvoiceImage
from invoice.permissions.purchase_invoice_image_permissions import (
    CanCreatePurchaseInvoiceImagePermission,
    CanDeletePurchaseInvoiceImagePermission
)
from invoice.serializers.purchase_invoice_image_serializers import (
    PurchaseInvoiceImageSerializer,
)
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveDeleteAPIView


class PurchaseInvoiceImageCreateAPIView(CustomCreateAPIView):
    serializer_class = PurchaseInvoiceImageSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreatePurchaseInvoiceImagePermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return PurchaseInvoiceImage.objects.get_image_of_branch(branch)


class PurchaseInvoiceImageRetrieveDeleteAPIView(CustomRetrieveDeleteAPIView):
    serializer_class = PurchaseInvoiceImageSerializer
    permission_class = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanDeletePurchaseInvoiceImagePermission
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return PurchaseInvoiceImage.objects.get_image_of_branch(branch)