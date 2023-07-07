from rest_framework import generics
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView

from product.filters.product_category_filters import ProductCategoryFilter
from product.models.product_category import ProductCategory
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from product.permissions.product_category_permissions import CanChangeProductCategoryPermission, CanCreateProductCategoryPermission, CanDeleteProductCategoryPermission, CanViewProductCategoryPermission

from product.serializers.product_category_serializers import ProductCategorySerializer


class ProductCategoryListAPIView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [CanViewProductCategoryPermission]
    filterset_class = ProductCategoryFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return ProductCategory.objects.get_category_of_branch(
            branch, fiscal_year
        ).order_by("-created_at")


class ProductCategoryCreateAPIView(CustomCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateProductCategoryPermission,
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return ProductCategory.objects.get_category_of_branch(branch, fiscal_year)


class ProductCategoryRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanViewProductCategoryPermission(),
            ]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanChangeProductCategoryPermission(),
            ]
        elif req_method == "DELETE":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanDeleteProductCategoryPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return ProductCategory.objects.get_category_of_branch(branch, fiscal_year)
