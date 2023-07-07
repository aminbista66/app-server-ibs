from rest_framework import generics
from inventory.filters.inventory_item_filters import InventoryItemFilter
from inventory.models.inventory_item import InventoryItem
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from inventory.permissions.inventory_item_permissions import (
    CanChangeInventoryItemPermission,
    CanCreateInventoryItemPermission,
    CanDeleteInventoryItemPermission,
    CanViewInventoryItemPermission,
)

from inventory.serializers.inventory_item_serializers import (
    InventoryItemCreateSerializer,
    InventoryItemSerializer,
)
from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView


class InventoryItemListAPIView(generics.ListAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [CanViewInventoryItemPermission]
    filterset_class = InventoryItemFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return InventoryItem.objects.get_item_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )


class InventoryItemCreateAPIView(CustomCreateAPIView):
    serializer_class = InventoryItemCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateInventoryItemPermission,
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return InventoryItem.objects.get_item_of_branch(branch, fiscal_year)


class InventoryItemRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    def get_serializer_class(self):
        req_method = self.request.method
        if req_method == "PUT" or req_method == "PATCH":
            return InventoryItemCreateSerializer
        else:
            return InventoryItemSerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewInventoryItemPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeInventoryItemPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteInventoryItemPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return InventoryItem.objects.get_item_of_branch(branch, fiscal_year)
