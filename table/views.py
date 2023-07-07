from rest_framework import generics
from rest_framework.filters import SearchFilter
from common.permissions import IsTenantAdminOrHasBranchAccessPermission

from logs.logs_mixins import CustomCreateAPIView, CustomRetrieveUpdateDeleteAPIView

from .models import TableCategory, Table

from .permissions import (
    CanViewTableCategoryPermission,
    CanChangeTableCategoryPermission,
    CanCreateTableCategoryPermission,
    CanDeleteTableCategoryPermission,
    CanViewTablePermission,
    CanCreateTablePermission,
    CanChangeTablePermission,
    CanDeleteTablePermission,
)

from .serializers import TableCategorySerializer, TableSerializer, TableCreateSerializer
from .filters import TableFilter


class TableCategoryListAPIView(generics.ListAPIView):
    serializer_class = TableCategorySerializer
    permission_classes = [CanViewTableCategoryPermission]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return TableCategory.objects.get_table_category_of_branch(branch).order_by(
            "-created_at"
        )


class TableCategoryCreateAPIView(CustomCreateAPIView):
    serializer_class = TableCategorySerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateTableCategoryPermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return TableCategory.objects.get_table_category_of_branch(branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class TableCategoryRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = TableCategorySerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewTableCategoryPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeTableCategoryPermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteTableCategoryPermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return TableCategory.objects.get_table_category_of_branch(branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class TableListAPIView(generics.ListAPIView):
    serializer_class = TableSerializer
    permission_classes = [CanViewTablePermission]
    filterset_class = TableFilter

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Table.objects.get_table_of_branch(branch).order_by("-created_at")


class TableCreateAPIView(CustomCreateAPIView):
    serializer_class = TableCreateSerializer
    permission_classes = [
        IsTenantAdminOrHasBranchAccessPermission,
        CanCreateTablePermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Table.objects.get_table_category_of_branch(branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class TableRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    def get_serializer_class(self):
        req_method = self.request.method
        if req_method == "PUT" or req_method == "PATCH":
            return TableCreateSerializer
        else:
            return TableSerializer

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewTablePermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeTablePermission()]
        elif req_method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteTablePermission()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Table.objects.get_table_of_branch(branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
