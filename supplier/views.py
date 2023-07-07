from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from common.permissions import IsTenantAdminOrHasBranchAccessPermission

from .models import Supplier
from .serializers import CreateSupplierSerializer, SupplierSerializer

from .permissions import (
    CanChangeSupplierPermission,
    CanCreateSupplierPermission,
    CanDeleteSupplierPermission,
    CanViewSupplierPermission,
)

from logs.logs_mixins import (
    CustomCreateAPIView,
    CustomRetrieveUpdateDeleteAPIView,
)


class SupplierCreateAPIView(CustomCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = CreateSupplierSerializer
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanCreateSupplierPermission]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Supplier.objects.get_supplier_of_branch(branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class SupplierListAPIView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsTenantAdminOrHasBranchAccessPermission, CanViewSupplierPermission]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        print("branch from request", branch)
        return Supplier.objects.get_supplier_of_branch(branch).order_by("-created_at")


class SupplierRetrieveUpdateDestroyAPIVIew(CustomRetrieveUpdateDeleteAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Supplier.objects.get_supplier_of_branch(branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanViewSupplierPermission()]
        elif self.request.method == "DELETE":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanDeleteSupplierPermission()]
        elif self.request.method == "PUT":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeSupplierPermission()]
        elif self.request.method == "PATCH":
            return [IsTenantAdminOrHasBranchAccessPermission(), CanChangeSupplierPermission()]
        else:
            return super().get_permissions()
