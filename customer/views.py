from rest_framework import generics
from rest_framework.filters import SearchFilter
from common.permissions import IsTenantAdminOrHasBranchAccessPermission
from customer.filters import CustomerFilter
from logs.logs_mixins import (
    CustomCreateAPIView,
    CustomRetrieveUpdateDeleteAPIView,
)
from .models import Customer
from .permissions import (
    CanChangeCustomerPermission,
    CanCreateCustomerPermission,
    CanDeleteCustomerPermission,
    CanViewCustomerPermission,
)
from .serializers import CustomerSerializer


class CustomerListAPIView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [CanViewCustomerPermission, IsTenantAdminOrHasBranchAccessPermission]
    filterset_class = CustomerFilter

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Customer.objects.get_customer_of_branch(branch).order_by("-created_at")


class CustomerRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDeleteAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Customer.objects.get_customer_of_branch(branch=branch)

    def get_permissions(self):
        req_method = self.request.method
        if req_method == "GET":
            return [CanViewCustomerPermission(), IsTenantAdminOrHasBranchAccessPermission()]
        elif req_method == "PUT" or req_method == "PATCH":
            return [
                CanChangeCustomerPermission(),
                IsTenantAdminOrHasBranchAccessPermission(),
            ]
        elif req_method == "DELETE":
            return [
                CanDeleteCustomerPermission(),
                IsTenantAdminOrHasBranchAccessPermission(),
            ]
        else:
            return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CustomerCreateAPIView(CustomCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [
        CanCreateCustomerPermission,
        IsTenantAdminOrHasBranchAccessPermission,
    ]

    def get_queryset(self):
        branch = self.request.GET.get("branch", None)
        return Customer.objects.get_customer_of_branch(branch=branch)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
