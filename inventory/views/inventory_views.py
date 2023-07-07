from rest_framework import generics
from inventory.filters.inventory_filters import InventoryFilter
from inventory.models.inventory import Inventory
from inventory.models.sub_inventory import SubInventory
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from inventory.permissions.inventory_permissions import (
    CanCreateInventoryPermission,
    CanDeleteInventoryPermission,
    CanViewInventoryPermission,
)

from inventory.serializers.inventory_serializers import (
    InventoryCreateSerializer,
    InventorySerializer,
)
from logs.logs_mixins import (
    CustomCreateAPIView,
    CustomRetrieveDeleteAPIView,
)


class InventoryListAPIView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [CanViewInventoryPermission]
    filterset_class = InventoryFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return Inventory.objects.get_inventory_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )


class InventoryCreateAPIView(CustomCreateAPIView):
    serializer_class = InventoryCreateSerializer
    common = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateInventoryPermission,
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return Inventory.objects.get_inventory_of_branch(branch, fiscal_year)


class InventoryRetrieveDeleteAPIView(CustomRetrieveDeleteAPIView):
    serializer_class = InventorySerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewInventoryPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteInventoryPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return Inventory.objects.get_inventory_of_branch(branch, fiscal_year)

    def perform_destroy(self, instance):
        item = instance.item
        instance.delete()

        sub_iventories = SubInventory.objects.filter(item=item)
        for sub_inventory in sub_iventories:
            sub_inventory.delete()
