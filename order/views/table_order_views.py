from rest_framework import generics
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from logs.logs_mixins import CustomCreateAPIView
from order.filters.table_order_filters import TableOrderFilter
from order.models import TableOrder
from order.permissions.table_order_permissions import (
    CanViewTableOrderPermissions,
    CanCreateTableOrderPermissions
)
from order.serializers.table_order_serializers import TableOrderCreateSerializer, TableOrderSerializer


class TableOrderListAPIView(generics.ListAPIView):
    permission_classes = [CanViewTableOrderPermissions]
    serializer_class = TableOrderSerializer
    filterset_class = TableOrderFilter

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return TableOrder.objects.get_table_order_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )
    

class TableOrderCreateAPIView(CustomCreateAPIView):
    serializer_class = TableOrderCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateTableOrderPermissions
    ]

    def get_queryset(self):
        branch = self.request.query_params.get("branch", None)
        fiscal_year = self.request.query_params.get("fiscal_year", None)
        return TableOrder.objects.get_table_order_of_branch(branch, fiscal_year).order_by(
            "-created_at"
        )