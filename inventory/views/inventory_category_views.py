from rest_framework import generics
from inventory.filters.inventory_category_filters import InventoryCategoryFilter
from inventory.models.inventory_category import InventoryCategory
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from inventory.permissions.inventory_category_permissions import (
    CanChangeInventoryCategoryPermission,
    CanCreateInventoryCategoryPermission,
    CanDeleteInventoryCategoryPermission,
    CanViewInventoryCategoryPermission,
)

from inventory.serializers.inventory_category_serializers import InventoryCategorySerializer
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView


class InventoryCategoryListAPIView(generics.ListAPIView):
    serializer_class = InventoryCategorySerializer
    permission_classes = [CanViewInventoryCategoryPermission]
    filterset_class = InventoryCategoryFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return InventoryCategory.objects.get_category_of_branch(
            branch, fiscal_year
        ).order_by("-created_at")


class InventoryCategoryCreateAPIView(CustomCreateAPIView):
    serializer_class = InventoryCategorySerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateInventoryCategoryPermission,
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return InventoryCategory.objects.get_category_of_branch(branch, fiscal_year)


class InventoryCategoryRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = InventoryCategorySerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanViewInventoryCategoryPermission(),
            ]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanChangeInventoryCategoryPermission(),
            ]
        elif req_method == "DELETE":
            return [
                IsTenantAdminOrHasBranchAccessPermission(),
                CanDeleteInventoryCategoryPermission(),
            ]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return InventoryCategory.objects.get_category_of_branch(branch, fiscal_year)
