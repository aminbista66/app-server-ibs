
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveDeleteAPIView
from product.models.product_image import ProductImage
from product.permissions.product_image_permissions import CanCreateProductImagePermission, CanDeleteProductImagePermission
from product.serializers.product_image_serializers import ProductImageSerializer



class ProductImageCreateAPIView(CustomCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateProductImagePermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return ProductImage.objects.get_image_of_branch(branch)


class ProductImageRetrieveDeleteAPIView(CustomRetrieveDeleteAPIView):
    serializer_class = ProductImageSerializer
    permission_class = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanDeleteProductImagePermission
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return ProductImage.objects.get_image_of_branch(branch)